# Super VJ Maker

**Apprendre le VJing avec 818 vraies loops, en appliquant les règles de montage d'un VJ en activité.**

Ce dépôt réunit deux choses :

1. **Les sources** — un outil qui télécharge, en format natif (.mp4 d'origine, sans ré-encodage), toute la bibliothèque de loops du lecteur [After TV](https://odcstudio.fr/after-tv/) (un projet de [@vj_rien_](https://www.instagram.com/vj_rien_/) et [@enjoy.dot](https://www.instagram.com/enjoy.dot/)).
2. **Les règles** — le rapport de ce qui pilote ces vidéos : les consignes de montage de VJ Rien (« Oscar »), dictées en langage naturel à un assistant de code, puis devenues l'algorithme d'After TV. On les lit, on les comprend, on les rejoue à la main dans son logiciel de VJ (Resolume, Modul8, VDMX, TouchDesigner, OBS…).

L'idée : au lieu de chercher des « astuces de VJ » partout, partir d'un **corpus réel** (818 loops, déjà classées : style, vitesse, thème, plans, tags) et d'un **jeu de règles testé en live** (un codex numéroté V1 à V88, avec les chiffres et les raisons de chaque règle), puis s'exercer.

> Les vidéos **ne sont pas dans ce dépôt** (≈ 12 Go) : on les télécharge soi-même avec l'outil ci-dessous. Voir [Droits et usage](#droits-et-usage).

---

## 1. Les sources : 818 loops

| | |
|---|---|
| Loops | 818 (484 en SD, 334 avec en plus une version HD) |
| Poids | ≈ 12 Go en « meilleure qualité » (HD quand elle existe, sinon SD) |
| Format | `.mp4` natif, servi tel quel par le site |
| Classement | style (house 62 · techno 327 · « les deux » 393), thème (films, humains, glitch, street, space, motion graphic 3d, pixel sorting…), vitesse (lent / moyen / rapide), rôle (drop, break, suspension, hyper), plans, tags visuels (`couleur:`, `forme:`, `sujet:`, `lumière:`…) |

Le téléchargeur écrit aussi `downloads/catalogue.csv` (ouvrable dans Excel/LibreOffice) : une ligne par loop avec son nom, son mood, son thème, son rôle, sa durée, ses tags. C'est la **fiche de classement** dont les règles se servent.

## 2. Les règles : ce que le VJ s'impose

Elles sont détaillées, sourcées et datées dans :

- 📘 [docs/RAPPORT-regles-montage.md](docs/RAPPORT-regles-montage.md) — **toutes les règles**, par thème, avec valeurs et citations ;
- 🛠 [docs/RAPPORT-construction-player.md](docs/RAPPORT-construction-player.md) — comment ces règles sont devenues un player et un algorithme.

Le résumé en 12 règles d'or à appliquer à la main :

1. **Un break, c'est une seule image**, qui joue d'un trait, sans la hacher ; un long break garde sa loop longtemps.
2. **Un drop, plusieurs images** : 1 à 3 écrans (jamais plus de 3), le nombre d'écrans change par phrases de 8 mesures ; après 16 mesures de drop on ne reste plus sur un seul écran.
3. **Une loop dominante par séquence** : elle joue des plans longs (≈ 3,5 mesures sur 4) ; les autres tournent autour en plans courts. Sans ça : « juste un catalogue de loops mises bout à bout ».
4. **Des allers-retours** : fais revenir 1 ou 2 loops déjà passées dans la séquence pour raconter quelque chose.
5. **Le tempo décide de la vitesse des images** : sous 100 BPM, que des loops lentes ; jusqu'à 125, pas de plans trop courts ; au-dessus, tout est permis.
6. **Un thème par écran** : jamais la même image deux fois ; et alterne régulièrement (≈ toutes les 3 min) entre « changer de thème » et « garder au moins un tag en commun ».
7. **Passe d'une loop à une voisine** : dans une collection classée par chapitres, on tire dans les ±10 loops proches, et 1 fois sur 5 on saute ailleurs pour avancer.
8. **Jamais une loop déjà vue** tant qu'il en reste d'autres ; pas plus de ≈ 3 loops neuves par minute ; un même film ne prend pas plus de ≈ 3 loops par demi-heure.
9. **Suspension dès que le kick manque** en plein drop (même 2 temps) ; **hyper** seulement quand le son est « plein » (beaucoup de notes ou de drums), 4 mesures puis long repos ; jamais d'hyper dans un break ni sous 100 BPM.
10. **Racontez en 4 chapitres** : humain → figuratif → texture → abstrait, puis **retour d'un coup aux visages** après 16 mesures ; jamais plus de 32 mesures sans visage.
11. **Respire** : 1 image sur 4 environ reste plusieurs coups en place pour casser l'alternance trop binaire. À 3 écrans, une image **par mesure**, pas par coup.
12. **Pas de son = noir** (après 4 s), en fondu, avec le nom du projet — pas une coupure.

## 3. Parcours d'apprentissage

Un exercice par niveau, chacun s'appuie sur une partie des règles :

| Niveau | Exercice | Règles | Filtre du téléchargeur utile |
|---|---|---|---|
| 1. Alterner | Deux loops qui alternent sur les temps (opacité 1/0), avec un morceau house à 126 BPM | 11 | `--mood house -q sd` |
| 2. Raconter | Une dominante + 2 satellites sur 8 mesures, avec un aller-retour | 3, 4 | `--theme films` |
| 3. Break / drop | Sur un morceau avec break : une image en break, 2-3 écrans au drop | 1, 2 | `--exclude-mask --exclude-oneshot` |
| 4. Lier les images | Choisir chaque loop suivante avec ≥ 1 tag en commun (ouvre `catalogue.csv`) | 6, 7 | — |
| 5. Tempo | Refaire l'exercice 3 à 90 BPM puis à 135 BPM en changeant de vivier | 5, 9 | colonne `vitesse` du CSV |
| 6. Chapitres | Construire une montée qui dérive vers l'abstrait, puis retour aux visages | 10 | colonne `theme` du CSV |
| 7. Ne rien répéter | Un set de 20 minutes sans loop revue et avec le quota de neuves | 8 | tout le catalogue |
| 8. Automatiser | Coder ses propres règles (voir les constantes dans les rapports) | toutes | — |

---

## 4. Mode d'emploi : télécharger les vidéos

### Option A — le `.exe` (Windows, rien à installer)

1. Ouvrir la page [Releases](../../releases/latest) et télécharger **`super-vj-downloader.exe`**.
2. Le placer dans un dossier avec beaucoup de place libre (≈ 12 Go en meilleure qualité).
3. **Double-cliquer** : l'outil pose 3 questions (qualité, style, liste ou téléchargement) puis télécharge dans un dossier `downloads/` à côté du `.exe`.

> Windows SmartScreen / l'antivirus peut avertir pour un `.exe` non signé : « Informations complémentaires » → « Exécuter quand même ». Le code source est dans ce dépôt ([after_tv_scraper.py](after_tv_scraper.py)), vous pouvez aussi le lancer avec Python (option B).

Le `.exe` accepte aussi les commandes de l'option C, depuis PowerShell / Terminal :

```powershell
.\super-vj-downloader.exe --dry-run
.\super-vj-downloader.exe -q both --mood house
```

### Option B — avec Python (3.8+, aucune dépendance à installer)

```bash
git clone https://github.com/<votre-compte>/super-vj-maker.git
cd super-vj-maker
python after_tv_scraper.py
```

Sans argument, le mode guidé s'ouvre comme avec le `.exe`.

### Option C — les commandes

Tester sans rien télécharger (liste + volume) :

```bash
python after_tv_scraper.py --dry-run
```

Tout télécharger, meilleure qualité (HD si elle existe, sinon SD) :

```bash
python after_tv_scraper.py
```

SD **et** HD :

```bash
python after_tv_scraper.py -q both
```

Seulement la SD (le plus léger, ≈ 9,5 Go) :

```bash
python after_tv_scraper.py -q sd
```

Seulement les loops de style techno (même filtre que le bouton du site) :

```bash
python after_tv_scraper.py --mood techno
```

Un thème précis, sans les masques ni les one-shots, 8 téléchargements en parallèle, dans un autre dossier :

```bash
python after_tv_scraper.py --theme films --exclude-mask --exclude-oneshot -w 8 -o D:\VJ\loops
```

Récupérer les nouveautés (relancer suffit : les fichiers déjà présents sont ignorés) :

```bash
python after_tv_scraper.py
```

…ou laisser tourner en vérifiant toutes les 30 minutes :

```bash
python after_tv_scraper.py --watch 30
```

### Toutes les options

| Option | Rôle | Défaut |
|---|---|---|
| `-o, --out DOSSIER` | dossier de sortie | `downloads` |
| `-q, --quality` | `best` · `sd` · `hd` · `both` | `best` |
| `--mood` | `tout` · `house` · `techno` (même règle que le site : une loop non jugée vaut « les deux ») | `tout` |
| `--theme NOM` | ne garder que ce thème (répétable) | — |
| `--exclude-old` | ignorer les loops marquées « old » | — |
| `--exclude-mask` | ignorer les masques (images à poser par-dessus) | — |
| `--exclude-oneshot` | ignorer les one-shots | — |
| `-w, --workers N` | téléchargements en parallèle | 4 |
| `--limit N` | ne télécharger que N fichiers (essai) | — |
| `--dry-run` | lister sans télécharger | — |
| `--watch MIN` | relire le manifeste toutes les MIN minutes | — |

### Ce qui est créé

```
downloads/
├── sd/                      loops SD :   « nom [id].mp4 »
├── hd/                      loops HD :   « nom [id].mp4 »
├── manifest.json            copie du catalogue du site (classement complet)
├── catalogue.csv            la même chose, lisible dans un tableur
└── erreurs.txt              seulement s'il y a eu des échecs
```

- Un téléchargement interrompu **reprend** là où il s'est arrêté (fichiers `.part`) : relancez la même commande.
- Les vidéos téléchargées sont **identiques octet pour octet** à celles du site.
- Le dossier `downloads/` est ignoré par git (`.gitignore`) : il ne part jamais dans le dépôt.

### Comment ça marche (et pourquoi un seul passage suffit)

Le site charge `config.json` → `manifest.json` (la liste de **toutes** les loops) puis lit les `.mp4` dans un bucket public. Les boutons House / Techno / Tout du site ne sont qu'un filtre dans le navigateur : le manifeste contient tout, l'outil le lit directement et applique le même filtre si vous le demandez. Pour de nouvelles loops, relancer l'outil suffit.

### Construire le `.exe` soi-même

```bash
pip install pyinstaller
pyinstaller --onefile --console --name super-vj-downloader after_tv_scraper.py
```

Le fichier est créé dans `dist/`.

### Dépannage

| Problème | Solution |
|---|---|
| Fenêtre qui se ferme tout de suite | lancer depuis PowerShell pour lire le message, ou double-cliquer (le mode guidé garde la fenêtre ouverte) |
| `✗ … 404` | une loop a été retirée du site : sans gravité, le reste continue |
| Téléchargement trop lent | augmenter `-w 8`, ou passer en `-q sd` |
| Manque de place | `--dry-run` donne le volume SD avant de commencer ; SD seule ≈ 9,5 Go, meilleure qualité ≈ 12 Go |

---

## Droits et usage

- Les **loops appartiennent à leurs auteurs** (VJ Rien / enjoy.dot et les ayants droit des images d'origine : extraits de films, clips, etc.). L'outil ne fait qu'accéder à ce que le site met publiquement à disposition du navigateur.
- Ce dépôt ne contient **aucune vidéo**. Téléchargez-les pour **votre étude personnelle** ; ne les redistribuez pas, ne les republiez pas, ne les utilisez pas en public sans l'accord de leurs auteurs.
- Les règles décrites dans les rapports sont tirées du code public d'After TV et des consignes que son auteur y a laissées en commentaires ; elles sont citées avec leur source. Ce projet n'est pas affilié à After TV.
- Soyez raisonnables avec le serveur : 4 téléchargements en parallèle par défaut, pas de `--watch` à une cadence très courte.

## Crédits

- **After TV** — a project by [@vj_rien_](https://www.instagram.com/vj_rien_/) and [@enjoy.dot](https://www.instagram.com/enjoy.dot/) : https://odcstudio.fr/after-tv/
- Radios du lecteur : Intergalactic FM.
