#!/usr/bin/env python3
"""
After TV scraper — télécharge toutes les vidéos (loops) du lecteur https://odcstudio.fr/after-tv/

Comment le site fonctionne :
  1. la page charge config.json  -> {"manifest": "manifest.json", "medias": "https://<bucket R2>/"}
  2. elle charge manifest.json   -> la liste complète des loops (id, nom, mood, thème, tags,
                                    video = version SD, video_hd = version HD si elle existe)
  3. les fichiers .mp4 sont lus directement dans le bucket R2 (« medias »).
Le sélecteur House / Techno / Tout n'est qu'un filtre côté navigateur : le manifeste contient
tout. Cet outil lit donc le manifeste, applique (ou non) le même filtre, et télécharge les .mp4
tels quels (format natif, aucun ré-encodage, octet pour octet).

Aucune dépendance : bibliothèque standard Python 3.8+.

Exemples :
  python after_tv_scraper.py --dry-run                 # liste + volume, rien n'est téléchargé
  python after_tv_scraper.py                           # tout, en meilleure qualité (HD sinon SD)
  python after_tv_scraper.py --quality both            # SD et HD
  python after_tv_scraper.py --mood house              # filtre comme le bouton « House »
  python after_tv_scraper.py --watch 30                # relance toutes les 30 min, ne prend que les nouveautés
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
import threading
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from urllib.parse import urljoin

SITE = "https://odcstudio.fr/after-tv/"
UA = "Mozilla/5.0 (after-tv-scraper)"
CHUNK = 1 << 20
MOODS = ("house", "techno")


# --------------------------------------------------------------------------- réseau
def http_get(url: str, timeout: int = 60) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Cache-Control": "no-cache"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def get_json(url: str):
    sep = "&" if "?" in url else "?"
    return json.loads(http_get(f"{url}{sep}_={int(time.time())}").decode("utf-8"))


def load_catalogue(site: str) -> tuple[list[dict], str]:
    """Retourne (loops, base_medias)."""
    site = site if site.endswith("/") else site + "/"
    cfg = get_json(urljoin(site, "config.json"))
    manifest_url = urljoin(site, cfg.get("manifest", "manifest.json"))
    medias = cfg.get("medias") or site
    if not medias.endswith("/"):
        medias += "/"
    medias = urljoin(site, medias)
    data = get_json(manifest_url)
    loops = data["loops"] if isinstance(data, dict) else data
    return loops, medias


# --------------------------------------------------------------------------- filtres
def accorde_au_mood(loop: dict, mood: str) -> bool:
    """Même règle que montage.js (accordeAuMood) : une loop sans mood ou « les deux » va partout."""
    if mood not in MOODS:
        return True  # « tout »
    pose = loop.get("mood")
    return pose in (None, "", "les deux") or pose == mood


def select(loops: list[dict], a: argparse.Namespace) -> list[dict]:
    out = []
    themes = {t.lower() for t in a.theme} if a.theme else None
    for l in loops:
        if not l.get("video"):
            continue
        if not accorde_au_mood(l, a.mood):
            continue
        if a.exclude_old and l.get("old"):
            continue
        if a.exclude_mask and l.get("mask"):
            continue
        if a.exclude_oneshot and l.get("one_shot"):
            continue
        if themes and str(l.get("theme", "")).lower() not in themes:
            continue
        out.append(l)
    return out


def plan_files(loops: list[dict], quality: str) -> list[dict]:
    """Une entrée par fichier à récupérer : {loop, rel (chemin distant), q ('sd'|'hd')}."""
    jobs = []
    for l in loops:
        hd = l.get("video_hd")
        if quality == "sd":
            picks = [("sd", l["video"])]
        elif quality == "hd":
            picks = [("hd", hd)] if hd else []
        elif quality == "both":
            picks = [("sd", l["video"])] + ([("hd", hd)] if hd else [])
        else:  # best
            picks = [("hd", hd)] if hd else [("sd", l["video"])]
        for q, rel in picks:
            jobs.append({"loop": l, "rel": rel, "q": q})
    return jobs


# --------------------------------------------------------------------------- fichiers
_BAD = re.compile(r'[<>:"/\\|?*\x00-\x1f]')


def safe_name(nom: str, id_: str, ext: str) -> str:
    nom = _BAD.sub("_", (nom or "").strip()).strip(". _")
    nom = re.sub(r"\s+", " ", nom)[:80].strip(". ")
    return f"{nom} [{id_}]{ext}" if nom else f"{id_}{ext}"


def target_path(out: Path, job: dict) -> Path:
    l = job["loop"]
    ext = Path(job["rel"]).suffix or ".mp4"
    return out / job["q"] / safe_name(l.get("nom", ""), l["id"], ext)


print_lock = threading.Lock()


def log(msg: str) -> None:
    with print_lock:
        print(msg, flush=True)


def download(url: str, dest: Path, expected: int | None, retries: int = 4) -> str:
    """Télécharge url -> dest via un .part (reprise possible). Retourne 'ok' | 'skip'."""
    if dest.exists() and (expected is None or dest.stat().st_size == expected):
        return "skip"
    dest.parent.mkdir(parents=True, exist_ok=True)
    part = dest.with_name(dest.name + ".part")
    last_err: Exception | None = None
    for attempt in range(1, retries + 1):
        try:
            have = part.stat().st_size if part.exists() else 0
            headers = {"User-Agent": UA}
            if have:
                headers["Range"] = f"bytes={have}-"
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=60) as r:
                status = getattr(r, "status", 200)
                total = None
                cr = r.headers.get("Content-Range")
                if status == 206 and cr and "/" in cr:
                    total = int(cr.rsplit("/", 1)[1])
                    mode = "ab"
                else:
                    cl = r.headers.get("Content-Length")
                    total = int(cl) if cl else None
                    mode, have = "wb", 0  # le serveur ignore Range : on repart de zéro
                with open(part, mode) as f:
                    while True:
                        buf = r.read(CHUNK)
                        if not buf:
                            break
                        f.write(buf)
            size = part.stat().st_size
            if total is not None and size != total:
                raise IOError(f"taille incomplète {size}/{total}")
            part.replace(dest)
            return "ok"
        except urllib.error.HTTPError as e:
            if e.code == 416:  # .part déjà complet ou corrompu
                part.unlink(missing_ok=True)
            last_err = e
            if e.code in (403, 404):
                break
        except Exception as e:  # réseau, timeout, taille…
            last_err = e
        time.sleep(min(2 ** attempt, 20))
    raise RuntimeError(str(last_err))


# --------------------------------------------------------------------------- sorties
def human(n: float) -> str:
    for u in ("o", "Ko", "Mo", "Go", "To"):
        if n < 1024 or u == "To":
            return f"{n:.1f} {u}" if u != "o" else f"{int(n)} o"
        n /= 1024
    return ""


def write_catalogue(out: Path, loops: list[dict]) -> None:
    out.mkdir(parents=True, exist_ok=True)
    (out / "manifest.json").write_text(json.dumps({"loops": loops}, ensure_ascii=False, indent=1), "utf-8")
    cols = ["id", "nom", "theme", "mood", "role", "duree_s", "octets", "old", "one_shot", "mask",
            "video", "video_hd", "styles", "tags"]
    with open(out / "catalogue.csv", "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f, delimiter=";")
        w.writerow(cols)
        for l in loops:
            row = []
            for c in cols:
                v = l.get(c, "")
                row.append(" | ".join(map(str, v)) if isinstance(v, list) else v)
            w.writerow(row)


def known_ids(out: Path) -> set[str]:
    p = out / "manifest.json"
    if not p.exists():
        return set()
    try:
        return {l["id"] for l in json.loads(p.read_text("utf-8"))["loops"]}
    except Exception:
        return set()


# --------------------------------------------------------------------------- run
def run_once(a: argparse.Namespace) -> int:
    out = Path(a.out)
    log(f"→ lecture du manifeste de {a.site}")
    loops, medias = load_catalogue(a.site)
    before = known_ids(out)
    new = [l for l in loops if l["id"] not in before] if before else []
    log(f"  {len(loops)} loops au total, bucket médias : {medias}")
    if before:
        log(f"  {len(new)} nouvelle(s) loop(s) depuis la dernière exécution")
        for l in new[:20]:
            log(f"    + {l['id']}  {l.get('nom', '')}")

    chosen = select(loops, a)
    jobs = plan_files(chosen, a.quality)
    sd_total = sum(j["loop"].get("octets") or 0 for j in jobs if j["q"] == "sd")
    n_hd = sum(1 for j in jobs if j["q"] == "hd")
    log(f"  sélection : {len(chosen)} loops, {len(jobs)} fichiers ({len(jobs) - n_hd} SD, {n_hd} HD)"
        f" — SD ≈ {human(sd_total)} (la taille des HD n'est connue qu'au téléchargement)")

    if not a.dry_run:
        write_catalogue(out, loops)

    if a.dry_run:
        for j in jobs:
            l = j["loop"]
            print(f"{j['q']}  {l['id']}  {l.get('mood', '-'):8}  {l.get('theme', '')[:24]:24}  {l.get('nom', '')}")
        return 0

    if a.limit:
        jobs = jobs[: a.limit]

    done = skipped = failed = 0
    errors: list[str] = []
    t0 = time.time()
    with ThreadPoolExecutor(max_workers=a.workers) as ex:
        futs = {}
        for j in jobs:
            dest = target_path(out, j)
            exp = j["loop"].get("octets") if j["q"] == "sd" else None
            futs[ex.submit(download, urljoin(medias, j["rel"]), dest, exp)] = (j, dest)
        for i, fu in enumerate(as_completed(futs), 1):
            j, dest = futs[fu]
            try:
                r = fu.result()
                if r == "ok":
                    done += 1
                    log(f"[{i}/{len(jobs)}] ✓ {dest.relative_to(out)}  ({human(dest.stat().st_size)})")
                else:
                    skipped += 1
            except Exception as e:
                failed += 1
                errors.append(f"{j['rel']}: {e}")
                log(f"[{i}/{len(jobs)}] ✗ {j['rel']} — {e}")

    log(f"\nTerminé en {time.time() - t0:.0f}s : {done} téléchargé(s), {skipped} déjà présent(s), {failed} échec(s)")
    log(f"Dossier : {out.resolve()}")
    if errors:
        (out / "erreurs.txt").write_text("\n".join(errors), "utf-8")
        log(f"Détail des erreurs : {out / 'erreurs.txt'}  (relancer la commande reprend là où ça s'est arrêté)")
    return 1 if failed else 0


def _choisir(question: str, options: list[tuple[str, str]], defaut: int = 1) -> str:
    print(f"\n{question}")
    for i, (_, libelle) in enumerate(options, 1):
        print(f"  {i}. {libelle}")
    while True:
        rep = input(f"Votre choix [{defaut}] : ").strip() or str(defaut)
        if rep.isdigit() and 1 <= int(rep) <= len(options):
            return options[int(rep) - 1][0]
        print("  Tapez un des numéros proposés.")


def interactif(a: argparse.Namespace) -> int:
    """Mode guidé : quelques questions, puis le téléchargement. Pour qui double-clique sur le .exe."""
    print("=" * 62)
    print(" SUPER VJ MAKER — téléchargeur des loops After TV")
    print(f" Source : {a.site}")
    print("=" * 62)
    a.quality = _choisir("Quelle qualité ?", [
        ("best", "Meilleure disponible : HD quand elle existe, sinon SD (recommandé)"),
        ("both", "SD et HD (plus lourd)"),
        ("sd", "SD seulement (le plus léger)"),
        ("hd", "HD seulement (uniquement les loops qui ont une HD)")])
    a.mood = _choisir("Quel style de loops ?", [
        ("tout", "Tout (house + techno + « les deux »)"),
        ("house", "House"),
        ("techno", "Techno")])
    a.dry_run = input("\nSimple liste, sans rien télécharger ? (o/N) ").strip().lower() in ("o", "oui", "y")
    print(f"\nLes vidéos iront dans : {Path(a.out).resolve()}\n")
    try:
        code = run_once(a)
    except Exception as e:
        print(f"\nErreur : {e}")
        code = 1
    input("\nAppuyez sur Entrée pour fermer.")
    return code


def main() -> int:
    p = argparse.ArgumentParser(description="Télécharge toutes les vidéos d'After TV (format natif).",
                                formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    p.add_argument("-o", "--out", default="downloads", help="dossier de sortie")
    p.add_argument("--site", default=SITE, help="URL de la page du lecteur")
    p.add_argument("-q", "--quality", choices=("best", "sd", "hd", "both"), default="best",
                   help="best = HD si dispo sinon SD ; hd = seulement celles qui ont une HD ; both = SD + HD")
    p.add_argument("--mood", choices=("tout", "house", "techno"), default="tout",
                   help="même filtre que les boutons du site")
    p.add_argument("--theme", action="append", help="ne garder que ce thème (répétable), ex. --theme films")
    p.add_argument("--exclude-old", action="store_true", help="ignorer les loops marquées « old »")
    p.add_argument("--exclude-mask", action="store_true", help="ignorer les masques")
    p.add_argument("--exclude-oneshot", action="store_true", help="ignorer les one-shots")
    p.add_argument("-w", "--workers", type=int, default=4, help="téléchargements en parallèle")
    p.add_argument("--limit", type=int, help="ne télécharger que N fichiers (test)")
    p.add_argument("--dry-run", action="store_true", help="lister sans télécharger")
    p.add_argument("--watch", type=float, metavar="MIN",
                   help="relire le manifeste toutes les MIN minutes pour récupérer les nouveautés")
    a = p.parse_args()

    for s in (sys.stdout, sys.stderr):  # consoles Windows en cp1252
        try:
            s.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass

    # Lancé sans argument (double-clic sur le .exe) : on pose les questions, et on garde la fenêtre ouverte.
    if len(sys.argv) == 1:
        return interactif(a)

    if not a.watch:
        return run_once(a)
    try:
        while True:
            run_once(a)
            log(f"… prochaine vérification dans {a.watch:g} min (Ctrl+C pour arrêter)\n")
            time.sleep(a.watch * 60)
    except KeyboardInterrupt:
        return 0


if __name__ == "__main__":
    sys.exit(main())
