# After TV — comment le player et son algorithme ont été construits à partir des règles

*Suite de [RAPPORT-regles-montage.md](RAPPORT-regles-montage.md). Source : le code public de https://odcstudio.fr/after-tv/ (page, JS, 22 modules Python, manifeste). Les parties privées (`app.py`, `prepare.py`, `deploie.py`, `docs/CODEX-VJ.md`, le dashboard Resolume) ne sont pas lisibles : ce qui les concerne est déduit des commentaires du code public.*

## 1. Idée directrice : « un seul programme » (codex V48)

Le player n'a **pas** été écrit à côté du dashboard de VJ : c'est le **dashboard lui-même, porté dans le navigateur**. Décision d'Oscar du 2026-11-12 (`docs/PLAN-AFTER-TV.md`) : « After TV tourne seul sur un site ; le code Python du dashboard tourne dans la page (Pyodide), un seul programme ».

Conséquence : chaque règle de la partie 1 existe **une seule fois**, en Python, et sert à la fois pour le set en live d'Oscar (Resolume/Arena, MIDI, platines) et pour le site. Le site n'est qu'un « écran » qui reçoit un état et l'affiche.

```
 DASHBOARD D'OSCAR (privé, FastAPI + Resolume + MIDI)        SITE PUBLIC (navigateur du visiteur)
 app.py : Engine ─────────── mêmes modules .py ───────────── pilote_web.py : Pilote (réécriture « au plus court »)
        live.py / outils_auto.py / sections.py / structure.py … identiques, copiés dans py/ au déploiement
```

Les endroits où le site **recopie** du code d'`app.py` sont balisés « Engine.<nom> » et « DETTE : à extraire d'app.py dans un module pur que les deux importeraient ».

## 2. Histoire de la construction (reconstituée par les dates et décisions du code)

| Étape | Ce que montrent les commentaires |
|---|---|
| **1. Le dashboard (sept. → oct.)** | Un moteur de VJ pour Resolume Arena : `LiveMode` (live.py) fait « alterner quelques loops sur la même ligne, à chaque coup on change de loop ET de repère ». Les règles de montage naissent là, avec les essais d'Oscar en jouant (2026-09-08 → 09-25). Les « motifs » étaient écrits à l'avance dans `settings.json` ; `LiveMode` les reconstruit à chaque clic. |
| **2. Autopilot** | Le dashboard apprend à jouer seul (`Engine.tick`, `outils_auto.py`) : demande du 2026-11-12 « utilise TOUS les outils du dashboard, sinon pas assez de variations ». La structure du morceau (break/drop, puis intro/couplet/refrain) est lue dans le son (`sections.py`, `structure.py`, `kick.py`). |
| **3. Première page « miroir »** | La page After TV **suit le dashboard** : il publie son état plusieurs fois par seconde (`miroir_web.py` → `{bpm, couches:{"1":{col,nom,opacite,blend,depart,t}…}}`), transmis par un relais (Cloudflare Worker `after-tv-relais`). `miroir.js` traduit cet état en couches vidéo. Ce chemin existe encore : `?direct=` ou `config.pilote`. |
| **4. Version de veille** | Quand le dashboard se tait : `montage.js` (`MontageSeul`) joue seule, avec un sous-ensemble de règles « réduites à ce qui tient sans le son d'Oscar ». Testée par `montage.test.mjs`. |
| **5. Le cerveau dans la page (2026-11-12 → 14)** | Pyodide charge les modules du dashboard ; l'oreille (tempo, kicks, genre) vient du projet open source *live-audio-analyzer* (hssnadr), **« épinglé sur un commit, jamais recopié »** après « accord de l'auteur du 2026-11-12 ». |
| **6. Page publique « toujours automatique » (2026-11-14 soir)** | Chaque visiteur a sa session : il choisit sa source de son (ordinateur, 3 radios Intergalactic FM, micro), son style, ses tags ; le dashboard d'Oscar n'est plus suivi (« Toujours automatique »). Console de debug pédagogique + documentation interactive pour un talk. |

Le même jour (2026-11-14) apparaissent presque simultanément V80–V88, l'écoute fine (« fais tout, et montre-moi petit à petit »), les quotas R1–R3 et l'interface visiteur : c'est le moment où le projet passe de l'outil de live à un produit public.

## 3. Architecture du player, couche par couche

### 3.1 Distribution et données

- **Hébergement** : page + manifeste sur Cloudflare Pages ; vidéos sur un bucket **R2** public (`config.json` → `medias`). Le `<video>` lit un autre domaine sans réglage CORS. Un Worker sert l'audience (`POST /after-tv/vu`) et l'ancien relais.
- **Manifeste** (`manifest.json`, 704 Ko, 818 loops) produit par `prepare.py` (privé) : une « fiche » par loop — `colonne` (rang dans la composition Resolume), `theme`, `mood`, `role/roles`, `vitesse`, `styles` (déjà corrigés à la main), `tags` (`famille:valeur`), `plans` (coupes en fractions), `old/one_shot/mask`, `duree_s`, `octets`, `video`, `video_hd`, `vignette`. **Les règles ne lisent que ces champs** : `pilote_web.fiche()` les remet au format que `live.py` attendait du `tags.json` du dashboard.
- **Pas dans le manifeste** (donc absents du site, marqués DETTE) : les **repères** posés dans Resolume (`reperes`) — `live.py` retombe sur des « parts égales de la loop » —, le chemin des fichiers (donc **pas de paires de montage dans le moteur web**, `paires = []`), la fiche visuelle complète.

### 3.2 La chaîne audio → décision (moteur.js + oreille_web.py)

```
getDisplayMedia (son système) | <audio> radio Icecast | getUserMedia (micro)
   → AudioContext + AudioWorklet feature-processor (hop 256, FFT 1024)
   → BeatTracker / KickDetector / DownbeatTracker (live-audio-analyzer)
   → toutes les 100 ms, lire() : pour chaque temps nouveau
        oreillePy.temps(...)         → partie du morceau, section break/drop, drop annoncé, section qui revient,
                                        + écoute fine (densité, motifs, matière, groove, montée, mémoire du set, voix/instruments)
        pilote.temps_js(t, kick, lecture, partie, bpm, rang)  → état à afficher (JSON, format miroir)
        pilote.reagir_js(r)          → réactions de fin de mesure (montage_ecoute)
   → emettre('temps', …) → la page applique l'état
```

- Le **détecteur de kick « maison »** (`kick.py`) est gardé comme référence car « tout a été réglé dessus » ; celui de la bibliothèque sert d'appoint (`kick_source = les_deux`, mesure du 2026-11-14).
- Le **genre** (YAMNet via MediaPipe) est lu toutes les 5 s et sert à choisir house/techno en mode « Auto » (V51 : « le style se lit aussi au son ») ; il est facultatif.
- **Tempo** : l'oreille, ou un **tap** du visiteur (médiane des écarts, ≥ 4 taps, tient 30 s, repris par l'oreille si > 15 % d'écart ; ÷2 / ×2 pour choisir l'octave).
- **Aucun appel payant** : la page ne reconnaît pas les morceaux (pas d'AudD) ; titre = infos de la radio, sinon rien.

### 3.3 Le cerveau (Python sous Pyodide)

`Pilote` (pilote_web.py) construit un `LiveWeb` (sous-classe de `live.LiveMode`) depuis le manifeste :

1. **Viviers** (`viviers()`) : pour chaque mode — montage (drop), break, suspension, hyper, one-shot, masque — la liste des colonnes dont les `roles` incluent ce mode, filtrée par *interdites* (NSFW, old), **mood**, **style** (familles ; repli si < 8 loops) et **tags voulus** (repli si < 6). Les replis sont tracés (`replis`) et affichés (« Not enough loops for these tags in some parts »).
2. **Pas par temps** (`Pilote.temps`) : dans l'ordre — bascule break/drop → `_limiter_sejour` (le séjour de 4 s) → `_break_alternance` → phases (superposition, chapitres/dérive, garantie d'un visage) → `_ouvrir_deux_ecrans` → `_outils_auto` → limite de durée du break → `sequencer.on_pulse(trigger)` → `_fire(step)` → `miroir_web.Miroir` → état.
3. **Sorties** : chaque pas du séquenceur émet les mêmes ordres que vers Resolume (`connect`, saut de repère, `set_opacity`, `set_blend`) ; `_SansResolume` les ignore et seul le **Miroir** les enregistre. C'est ce qui garantit que l'état publié est « EXACTEMENT celui que le dashboard publie ».

Ce qui **n'a pas été repris** dans le port (« n'a pas de sens sans Resolume ni manette ») : strobe, sur-mesure, mouche, MANO, MIDI, one-shot (il faut `phrase.Phrase` et la longueur des loops en mesures) ; la densité du son pour le séjour des satellites (« non mesurée dans la page »).

### 3.4 L'algorithme de choix de la loop suivante (`live._free_column` → `_tire_colonne`)

C'est la traduction directe des règles, sous forme de **filtres successifs qu'on relâche** « plutôt que de figer l'écran : le montage ne s'arrête jamais » :

```
_free_column(pres_de, remplace)
 ├─ R1 (V86) quota de « neuves » atteint ?  → _tirer_retour : une loop récente du vivier revient
 ├─ 1 fois sur 10 (V81) → _tirer_invitee : une suspension / un one-shot passe dans le montage
 └─ _tire_colonne :
     1. vivier = pool du mode (break/suspension/hyper) ou montage ; si « accent » (famille du morceau)
        et aucune loop de la famille à l'écran → on ne prend que l'accent
     2. exclure ce qui est déjà à l'écran ; freiner les « DM… » (≤ 1 sur 12)
     3. V66  permises_au_tempo : vitesse ↔ BPM (avant le non-retour)
     4. V21  non-retour : ne garder que les « jamais vues de ce cycle » (sinon vider le cycle)
     5. R3 (V88) _sous_plafond : un film ne dépasse pas 3 loops / 30 min
     6. au_tempo : les plus lentes d'abord ; un thème par écran (règle « theme »)
     7. paliers / chapitres : le palier d'abstraction visé, avec `_fraiches` (pas d'usure)
     8. V52  paire de montage : avec une chance, la partenaire passe avant tout
     9. règle « tags » (alterne toutes les 180 s avec « theme », V47) : `_mieux_liees`
        = au moins un tag en commun, pondérés par rareté (log n/porteurs), voisine = bonus
    10. même composition, autre thème (60 %)
    11. voisinage ±10 colonnes (80 %), même thème d'abord ; sinon n'importe où
    12. `_prendre` : R2 (V87) les moins montrées (tolérance 15 s) → les moins vues →
        la matière du son départage les égales → favorites d'abord → `random.choice`
```

Chaque règle de la partie 1 est donc une **ligne** de ce pipeline ; l'ordre de ces lignes encode les **priorités** (la paire validée par Oscar passe avant le thème et le palier ; le tempo passe avant le non-retour ; le non-retour passe avant les préférences de voisinage). Ces priorités viennent des défauts mesurés : « sur un morceau lent, une loop lente déjà passée vaut mieux qu'une rapide jamais vue ».

### 3.5 Le rythme : le séquenceur (`sequencer.py`)

- Un **motif** (`Pattern`) = suite de `Step(colonne, repère, hold)` avec une cadence (`kick`, `hihat`, `beat`, `2beats`, `bar`). Un changement de motif attend le prochain temps 1 de la mesure (« sinon le montage saute au milieu d'un pas et ça s'entend »).
- `LiveMode._motif()` construit le motif selon le mode : **break** = un seul pas, la loop court d'un trait depuis un repère tiré au hasard ; **dominante** = `_pas_dominante` (plans longs pour la dominante, 2 temps pour les satellites) ; **normal** = un pas par image, une image par coup à 2 écrans, **une par mesure à partir de 3** (« sinon ça défile trop vite »).
- **Respiration** (`_respirer`) : 25 % des pas tiennent 2 à `hold_max` coups, pour casser l'alternance binaire.

### 3.6 Les outils d'autopilot (`outils_auto.py`)

Un `Pilote` d'outils **décide sans jouer** : à chaque temps il reçoit un `Contexte` (mode, nombre d'écrans, partie du morceau, hi-hats, densité *pleine/montante*, kick manquant, tempo, outils disponibles) et rend des **ordres avec leur raison en clair**. `_jouer_ordre` les exécute par les mêmes chemins que les boutons d'Oscar. Chaque outil a un « AUTO » : allumé, l'autopilot s'en sert ; éteint, c'est la main d'Oscar qui prime (« un mode posé à la main n'est jamais touché »). Garde-fous explicites : un mode posé par le pilote (hyper, suspension) ne tient jamais sans fin (rendu après `HYPER_MESURES` / `SUSPENSION_MAX_MESURES`), et un mode ne change qu'après `MODE_TENIR` = 4 mesures (sinon différé).

### 3.7 L'écran : double buffer vidéo et gardiens (`index.html`)

- **Couches** : jusqu'à 3 `div` (une par écran), chacune avec **deux `<video>` jumeaux** (`videos[0/1]`). Le visible joue pendant que le jumeau charge la loop suivante ; on bascule seulement quand `quandImagePrete()` confirme qu'une image est *réellement* affichable (`readyState ≥ 2`, `requestVideoFrameCallback`). Origine : « des vidéos se lancent pas, ça reste figé à la frame 1 » (2026-11-12).
- **Une préparation en cours va toujours au bout** : en hyper, un saut de repère toutes les 0,5 s relançait la vidéo cachée avant qu'elle soit prête → écran noir. Maintenant une couche ne prépare qu'une chose à la fois et « rattrape » la dernière demande ensuite.
- **Mêmes loops, autre repère** : si le repère voulu est déjà en mémoire (`buffered`), on saute immédiatement (`currentTime`).
- **Gardien toutes les 500 ms** : vidéo à l'écran qui n'avance plus → `play()` ; figée 5 cycles → le jumeau recharge à la bonne position. Abandon après 8 s, nouvel essai après 5 s.
- **Fusion** : opacité de la couche ; fusion « 50 Add » d'Arena traduite en CSS `mix-blend-mode: plus-lighter` (le dessous + opacité × la couche), « Alpha » = normal.
- **Anti-noir** : un état sans couche visible est toléré 1,5 s (un coup de strobe) ; au-delà, on garde la dernière image valable ou on joue la veille. **Pas de son > 4 s** → `body.silence` → fondu vers le noir « After TV » (V74, « avec un fade out vers le noir, pas en coupure »).
- **Qualité adaptative (« HD auto »)** : toutes les 45 s, une requête `Range` de 2 Mo sur un fichier HD tiré au hasard mesure le débit ; HD au-dessus de **12 Mbit/s**, retour en SD sous **9** (hystérésis). Un fichier HD absent de R2 retombe aussitôt sur la SD (`hdAbsent`). Interrupteur visiteur : HD auto allumé par défaut / SD seulement.

### 3.8 Les trois niveaux de repli (« jamais un noir muet »)

1. **Moteur complet** (Pyodide + son du visiteur) ;
2. **Radio seule** : si le moteur ne se charge pas (Pyodide, réseau), la radio lancée dans le clic joue sans analyse, avec une ligne d'explication (`moteurEchec`) ;
3. **Veille** (`montage.js`) : deux loops liées qui alternent sur les temps, avec voisinage, tags en commun, non-retour de 40 loops, paires de montage.

La veille reprend la main si le moteur du visiteur se tait 3 s ; le dashboard, s'il publie, passe devant tout.

### 3.9 Interface et mise au point

- **Entrée** pensée autour des contraintes navigateur : le partage de son (`getDisplayMedia`) n'existe que sur Chrome/Edge bureau ; Safari exige un geste (donc `audio.play()` et `AudioContext` créés *dans le clic*) ; téléphone = micro par défaut ; suggestion de la radio après 5 s sans son (visible 8 s, écartée une fois pour la visite).
- **Réglages** gardés dans `localStorage` (style House par défaut, tags, coupes rapides, HD, source, radio), jamais envoyés. Audience : un battement toutes les 5 min (minutes *visibles*), identifiant de visite aléatoire, pays ajouté côté Worker.
- **Console de debug pédagogique** (« entendu → déduit → effet à l'écran → règle d'Oscar ») : chaque règle qui joue est affichée avec son numéro de codex ; la phrase d'origine d'Oscar est « gardée pour la provenance ». C'est un outil de **traçabilité des consignes** : le code sait dire *pourquoi* une loop est entrée (`dernier_lien`, `journal`, `_noter`).
- **Tests et mesures** : `node --test` (montage, miroir, réglages, radio, moteur), des « bancs » sur de vrais sets (Justice, Sawf…), des mesures de direct (« 7 hypers en 8,7 min », « 19 retours de la même loop en 20 min »).

## 4. Comment une consigne devient du code (le cycle de « vibe coding »)

Le dépôt montre un schéma répété :

1. **Dictée en langage naturel**, souvent critique ou perceptive : « les loops changent trop vite », « je ne vois toujours pas les modes suspension et hyper automatisés ».
2. **Interprétation + numéro de codex** (`Vxx`) avec une règle écrite en clair (colonne « Règle » de `CODEX-VJ.md`) ; la citation d'origine reste dans un commentaire.
3. **Constantes nommées en tête de fichier** « pour qu'Oscar les corrige » (`HYPER_REPOS_MESURES = 32`, `CHANCE_PAIRE = 1/6`…), ce qui rend la règle réglable sans lire l'algorithme.
4. **Mesure sur un enregistrement ou un direct**, puis ajustement du chiffre (« une par minute était trop intense »).
5. **Statut** : « PROPOSITION, à valider par Oscar » → validée → entre au codex. La « page des choix » (2026-11-12) formalise ces validations (A1, D2…).
6. **Réutilisation** : un module pur (« aucune horloge, aucun fil, aucun fichier ») qui se teste en lui donnant des temps — ce qui permet de rejouer les mêmes règles dans Resolume, dans Pyodide et dans les tests.

Un exemple complet — **« Les loops changent trop vite »** (2026-11-12) :
> consigne : « chaque séquence doit avoir une loop dominante, sinon c'est juste un catalogue » → V68 → `live.set_dominante` + `_pas_dominante` (3,5 mesures/4 pour la dominante, 2 temps pour un satellite) → `pilote_web._pas_aftertv` : la dominante ne sort que quand elle a tenu `min(3 × durée, 60 s)` → console : « loop dominante : {nom} ».

## 5. Écarts entre l'intention et le code actuel

- **Paires de montage** : actives dans la veille JS, **désactivées** dans le moteur Pyodide (manque de chemins dans le manifeste).
- **Repères** : absents du manifeste → les sauts « par repères d'Oscar » deviennent des **parts égales** de la loop.
- **One-shot, strobe** : non portés ; **densité** du son seulement partielle pour la durée des satellites.
- **Règles « propositions »** (V55–V63) : le code les applique mais les signale comme à valider ; des chiffres bougent (ex. suspension passée de « 4 mesures de tenue » à « 2 temps » le 2026-11-14).
- **Dette technique déclarée** : fonctions « Engine.* » recopiées au lieu d'être importées ; `app.py` ne s'importe pas hors du serveur (FastAPI, carte son, MIDI, Resolume).
- **Dépendances externes** : Pyodide v0.27.7 et live-audio-analyzer (commit épinglé) chargés depuis jsDelivr ; radios Intergalactic FM (CORS ouvert) ; YAMNet via MediaPipe.

## 6. Pour aller plus loin (si on veut reproduire ou étudier le montage)

- Le **manifeste** (déjà dans `downloads/manifest.json` + `catalogue.csv` grâce au scraper) suffit pour recréer les viviers (mood, familles, vitesse, rôles, tags, colonnes).
- Les modules Python sont publics sous `https://odcstudio.fr/after-tv/py/*.py` ; ils tournent sous CPython (ils sont conçus pour être testés ainsi, avec `numpy`).
- Non récupérables depuis le site : le codex complet (`docs/CODEX-VJ.md`), les repères Resolume, `prepare.py`, la composition d'origine.
