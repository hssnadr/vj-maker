# 🎛️ VJ Maker

**Apprends le VJing avec 818 vraies loops, en appliquant les règles de montage d'un VJ en activité.**

Tu veux apprendre à *monter des images sur de la musique en live* ? Ici, tu as :

1. **Les sources** — un outil qui télécharge toute la bibliothèque de loops du lecteur [After TV](https://odcstudio.fr/after-tv/) (un projet de [@vj_rien_](https://www.instagram.com/vj_rien_/) et [@enjoy.dot](https://www.instagram.com/enjoy.dot/)), en **format natif** : les `.mp4` d'origine, sans ré-encodage.
2. **Les règles** — ce qui pilote ces vidéos : les consignes de montage de VJ Rien (« Oscar »), dictées *à l'oral* à une IA (le fameux **vibe coding**), puis devenues l'algorithme d'After TV. Tu les lis, tu les comprends, tu les rejoues **à la main** dans ton logiciel (Resolume, Modul8, VDMX, TouchDesigner, OBS…).
3. **Le glossaire** — parce que ces règles parlent musique, VJing *et* programmation, il y a un [**guide du jargon**](docs/GLOSSAIRE.md) qui explique tout simplement.

L'idée : au lieu de chercher des « astuces de VJ » partout, tu pars d'un **vrai corpus** (818 loops déjà classées par style, vitesse, thème, tags) et d'un **jeu de règles testé en live** (un carnet numéroté V1 → V88, avec le chiffre et la raison de chaque règle). Puis tu t'exerces.

> 📦 **Les vidéos ne sont pas dans ce dépôt** (≈ 12 Go) : tu les télécharges toi-même avec l'outil. Voir [Droits et usage](#droits-et-usage).

**Plan** : [1. Les sources](#1-les-sources--818-loops) · [2. Le jargon express](#2-le-jargon-express) · [3. Les règles](#3-les-règles--ce-que-le-vj-simpose) · [4. C'est quoi le vibe coding ?](#4-cest-quoi-le-vibe-coding-et-comment-lire-une-consigne) · [5. Parcours d'apprentissage](#5-parcours-dapprentissage) · [6. Télécharger les vidéos](#6-mode-demploi--télécharger-les-vidéos) · [Droits](#droits-et-usage)

---

## 1. Les sources : 818 loops

| | |
|---|---|
| Loops | 818 (484 en SD ; 334 avec en plus une version HD) |
| Poids | ≈ 12 Go en « meilleure qualité » (HD quand elle existe, sinon SD) ; ≈ 9,5 Go en SD seule |
| Format | `.mp4` natif, servi tel quel par le site |
| Classement | **style** (house 62 · techno 327 · « les deux » 393 · non jugées 36), **thème** (films, humains, glitch, street, space, motion graphic 3d, pixel sorting…), **vitesse** (lent / moyen / rapide), **rôle** (drop, break, suspension, hyper), **plans**, **tags visuels** (`couleur:`, `forme:`, `sujet:`, `lumière:`…) |

Le téléchargeur écrit aussi `downloads/catalogue.csv` (ouvrable dans Excel ou LibreOffice) : **une ligne par loop**, avec son nom, son mood, son thème, son rôle, sa durée et ses tags. C'est la **fiche de classement** dont se servent les règles. Garde-la ouverte quand tu t'exerces !

## 2. Le jargon express

Tu verras ces mots partout. Le [**glossaire complet**](docs/GLOSSAIRE.md) en explique une soixantaine, avec des exemples.

| Mot | En deux mots |
|---|---|
| **Loop** | Une courte vidéo qui boucle. |
| **BPM** | Le tempo : 126 BPM = 126 battements par minute. |
| **Temps / mesure** | Un temps = un battement ; une mesure = 4 temps. |
| **Kick** | La grosse caisse, le « boum » régulier. |
| **Drop** | Le moment fort, quand tout revient en force. |
| **Break** | La pause : le kick disparaît. |
| **Couche / écran** | Une piste vidéo. On en empile jusqu'à 3. |
| **Opacité / fusion** | La transparence d'une couche / la façon de la mélanger avec les autres (*Alpha* = recouvre, *Add* = les couleurs s'additionnent). |
| **Vivier** | La liste des loops qui ont le droit de jouer à un moment donné. |
| **Dominante** | La loop « personnage principal » d'une séquence. |
| **Tag** | Une étiquette du type `couleur:désaturé`. |
| **Codex (V68…)** | Le carnet de règles : un numéro = une décision. |

> ⏱️ **Pense en mesures, pas en secondes.** À 126 BPM : 1 temps ≈ 0,5 s · 1 mesure ≈ 1,9 s · 8 mesures ≈ 15 s. (La calculette est dans le [glossaire](docs/GLOSSAIRE.md#9-calculette-bpm--secondes).)

## 3. Les règles : ce que le VJ s'impose

Elles sont détaillées, sourcées et datées dans :

- 📘 [**docs/RAPPORT-regles-montage.md**](docs/RAPPORT-regles-montage.md) — toutes les règles, par thème, avec les valeurs ;
- 🛠 [**docs/RAPPORT-construction-player.md**](docs/RAPPORT-construction-player.md) — comment ces règles sont devenues un player et un algorithme ;
- 🔤 [**docs/GLOSSAIRE.md**](docs/GLOSSAIRE.md) — pour tout décoder.

Le résumé : **12 règles d'or** à appliquer à la main.

| # | Règle | Pourquoi ça marche |
|---|---|---|
| 1 | **Un break, c'est une seule image**, qui joue longtemps et sans être hachée. | La pause sonore appelle une pause visuelle : on laisse respirer. |
| 2 | **Un drop, plusieurs images** : 1 à 3 écrans, jamais plus de 3. Après 16 mesures de drop, on ne reste plus sur un seul écran. | Le drop est le moment de l'énergie. |
| 3 | **Une loop dominante par séquence** : elle joue des plans longs (≈ 3,5 mesures sur 4) ; les autres tournent autour en plans courts. | Sans personnage principal, ce n'est qu'un catalogue d'images. |
| 4 | **Des allers-retours** : refais passer 1 ou 2 loops déjà vues dans la séquence. | Les retours créent un fil narratif. |
| 5 | **Le tempo décide de la vitesse des images** : sous 100 BPM, que des loops lentes ; jusqu'à 125, pas de plans très courts ; au-dessus, tout est permis. | Des images trop rapides sur un morceau lent se « battent » avec la musique. |
| 6 | **Un thème par écran**, et alterne (≈ toutes les 3 min) entre « changer de thème » et « garder au moins un tag en commun ». | Jamais la même image deux fois ; un lien visible d'une image à l'autre. |
| 7 | **Passe d'une loop à sa voisine** (±10 loops dans ta collection classée) ; 1 fois sur 5, saute ailleurs. | On reste cohérent sans tourner en rond. |
| 8 | **Ne reprends pas une loop vue** tant qu'il en reste ; ≈ 3 loops neuves par minute au plus ; un même film ne prend pas plus de ≈ 3 loops par demi-heure. | Un catalogue brûlé en 45 min n'a plus rien à offrir. |
| 9 | **Suspension dès que le kick manque** en plein drop (même 2 temps) ; **hyper** seulement quand le son est « plein », 4 mesures puis long repos ; jamais d'hyper dans un break ni sous 100 BPM. | Un effet fort doit rester court et rare. |
| 10 | **Raconte en 4 chapitres** : humain → figuratif → texture → abstrait, puis retour **d'un coup** aux visages après 16 mesures ; jamais plus de 32 mesures sans visage. | Les visages accrochent l'œil, l'abstrait le fait voyager. |
| 11 | **Respire** : 1 image sur 4 environ reste plusieurs coups en place. À 3 écrans, une image **par mesure**, pas par coup. | Casse l'alternance « métronome ». |
| 12 | **Pas de son = noir** (après 4 s), en fondu, avec le nom du projet. | Mieux vaut un noir assumé qu'une image sans raison. |

## 4. C'est quoi le vibe coding, et comment lire une consigne ?

**Vibe coding** = construire un programme en **décrivant ce qu'on veut avec ses mots** à une IA, sans écrire le code soi-même. On parle, on regarde, on corrige. Le VJ qui a bâti After TV l'a fait comme ça : ses règles sont des **phrases dites à l'oral**, que l'IA a transformées en code.

Chaque règle suit presque toujours le même chemin :

```
 1. Ce que le VJ ressent ou veut         ("ça change trop vite")
 2. Un numéro de codex                    (V68)           ← la décision est gardée
 3. La règle en clair, avec un chiffre   ("une loop dominante, 3,5 mesures sur 4")
 4. Une constante réglable dans le code  (DOMINANTE_BLOC_MESURES = 4)
 5. Une mesure sur un vrai set           (la preuve que le chiffre est bon)
```

Un exemple, **V68 — « les images changent trop vite »** : le VJ constate qu'on n'a pas le temps de raconter quelque chose. La règle devient : *la première loop est la dominante, elle joue des plans longs ; les autres passent autour en plans courts.* Dans le code : un bloc de 4 mesures, la dominante en prend 3,5, un satellite 2 temps.

👉 Le [glossaire](docs/GLOSSAIRE.md#7-lire-une-règle-ligne-par-ligne) décortique 3 règles de cette façon, et explique [comment écrire ton propre prompt de VJ](docs/GLOSSAIRE.md#8-écrire-ton-propre-prompt-de-vj) : *ce que je vois → ce que je veux → un chiffre → les exceptions → comment vérifier*.

## 5. Parcours d'apprentissage

Un exercice par niveau, chacun s'appuie sur une partie des règles :

| Niveau | Exercice | Règles | Filtre du téléchargeur utile |
|---|---|---|---|
| 1. Alterner | Deux loops qui alternent sur les temps (opacité 100 % / 0 %), sur un morceau house à 126 BPM. | 11 | `--mood house -q sd` |
| 2. Raconter | Une dominante + 2 satellites sur 8 mesures, avec un aller-retour. | 3, 4 | `--theme films` |
| 3. Break / drop | Sur un morceau avec break : une image en break, 2-3 écrans au drop. | 1, 2 | `--exclude-mask --exclude-oneshot` |
| 4. Lier les images | Choisis chaque loop suivante avec ≥ 1 tag en commun (ouvre `catalogue.csv`). | 6, 7 | — |
| 5. Tempo | Refais l'exercice 3 à 90 BPM puis à 135 BPM en changeant de sélection. | 5, 9 | colonne `vitesse` du CSV |
| 6. Chapitres | Construis une montée qui dérive vers l'abstrait, puis retour aux visages. | 10 | colonne `theme` du CSV |
| 7. Ne rien répéter | Un set de 20 min sans loop revue, avec le quota de neuves. | 8 | tout le catalogue |
| 8. Automatiser | Code tes propres règles (les constantes sont listées dans les rapports). | toutes | — |

---

## 6. Mode d'emploi : télécharger les vidéos

### Option A — le `.exe` (Windows, rien à installer)

1. Va sur la page [**Releases**](../../releases/latest) et télécharge **`vj-downloader.exe`**.
2. Mets-le dans un dossier avec beaucoup de place libre (≈ 12 Go en meilleure qualité).
3. **Double-clique** : l'outil te pose 3 questions (qualité, style, liste ou téléchargement) puis télécharge dans un dossier `downloads/` à côté du `.exe`.

> ⚠️ Windows SmartScreen ou ton antivirus peut avertir pour un `.exe` non signé : « Informations complémentaires » → « Exécuter quand même ». Le code est lisible dans [after_tv_scraper.py](after_tv_scraper.py), tu peux aussi le lancer avec Python (option B).

Le `.exe` accepte aussi les commandes de l'option C, depuis PowerShell :

```powershell
.\vj-downloader.exe --dry-run
```
```powershell
.\vj-downloader.exe -q both --mood house
```

### Option B — avec Python (3.8+, aucune dépendance)

```bash
git clone https://github.com/<ton-compte>/vj-maker.git
cd vj-maker
python after_tv_scraper.py
```

Sans argument, le mode guidé s'ouvre, comme avec le `.exe`.

### Option C — les commandes

Tester sans rien télécharger (liste + volume) :

```bash
python after_tv_scraper.py --dry-run
```

Tout télécharger, en meilleure qualité (HD si elle existe, sinon SD) :

```bash
python after_tv_scraper.py
```

SD **et** HD :

```bash
python after_tv_scraper.py -q both
```

SD seulement (le plus léger) :

```bash
python after_tv_scraper.py -q sd
```

Seulement le style techno (même filtre que le bouton du site) :

```bash
python after_tv_scraper.py --mood techno
```

Un thème précis, sans masques ni one-shots, 8 téléchargements en parallèle, dans un autre dossier :

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

- Un téléchargement interrompu **reprend** là où il s'est arrêté (fichiers `.part`) : relance la même commande.
- Les vidéos sont **identiques octet pour octet** à celles du site.
- Le dossier `downloads/` est ignoré par git (`.gitignore`) : il ne part jamais dans le dépôt.

### Pourquoi un seul passage suffit

Le site charge un fichier `manifest.json` qui liste **toutes** les loops, puis lit les `.mp4` dans un bucket public. Les boutons House / Techno / Tout du site ne font que filtrer dans ton navigateur : le manifeste contient tout. L'outil le lit directement. Pour de nouvelles loops, relance simplement l'outil.

### Construire le `.exe` toi-même

```bash
pip install pyinstaller
pyinstaller --onefile --console --name vj-downloader after_tv_scraper.py
```

Le fichier est créé dans `dist/`.

### Dépannage

| Problème | Solution |
|---|---|
| La fenêtre se ferme tout de suite | Lance depuis PowerShell pour lire le message, ou double-clique (le mode guidé garde la fenêtre ouverte). |
| `✗ … 404` | Une loop a été retirée du site : sans gravité, le reste continue. |
| Téléchargement trop lent | Monte `-w 8`, ou passe en `-q sd`. |
| Manque de place | `--dry-run` donne le volume SD avant de commencer ; SD seule ≈ 9,5 Go, meilleure qualité ≈ 12 Go. |

---

## Droits et usage

- Les **loops appartiennent à leurs auteurs** (VJ Rien / enjoy.dot et les ayants droit des images d'origine : extraits de films, clips, etc.). L'outil ne fait qu'accéder à ce que le site met publiquement à disposition du navigateur.
- Ce dépôt ne contient **aucune vidéo**. Télécharge-les pour **ton étude personnelle** ; ne les redistribue pas, ne les republie pas, ne les utilise pas en public sans l'accord de leurs auteurs.
- Les règles décrites dans les rapports sont tirées du code public d'After TV et des commentaires que son auteur y a laissés. Ce projet n'est pas affilié à After TV.
- Sois raisonnable avec le serveur : 4 téléchargements en parallèle par défaut, pas de `--watch` à une cadence très courte.

## Crédits

- **After TV** — a project by [@vj_rien_](https://www.instagram.com/vj_rien_/) and [@enjoy.dot](https://www.instagram.com/enjoy.dot/) : https://odcstudio.fr/after-tv/
- Radios du lecteur : Intergalactic FM.
