# Le glossaire : décoder le jargon des règles

Les règles d'After TV sont écrites par un VJ pour un assistant de code. Elles mélangent donc **trois langues** : celle de la musique, celle du VJing et celle du « vibe coding ». Pas de panique : tout est expliqué ici, avec des exemples. Garde cette page ouverte pendant que tu lis [les règles](RAPPORT-regles-montage.md).

**Sommaire** : [1. La musique](#1-la-musique-en-3-minutes) · [2. La structure d'un morceau](#2-la-structure-dun-morceau) · [3. Les images](#3-les-images-le-vocabulaire-vj) · [4. Les 4 modes](#4-les-4-modes-de-montage) · [5. L'algorithme](#5-les-mots-de-lalgorithme) · [6. Vibe coding](#6-le-vibe-coding-cest-quoi) · [7. Lire une règle](#7-lire-une-règle-ligne-par-ligne) · [8. Écrire ton prompt](#8-écrire-ton-propre-prompt-de-vj) · [9. Calculette BPM](#9-calculette-bpm--secondes)

---

## 1. La musique en 3 minutes

| Mot | Ça veut dire | Pour s'en souvenir |
|---|---|---|
| **BPM** | *Beats per minute* : le tempo. 126 BPM = 126 battements par minute. | La vitesse du « toc-toc-toc » du pied. |
| **Temps** (*beat*) | Un battement. C'est le « 1, 2, 3, 4 » que tu comptes en tapant du pied. | Une unité de base pour tout le montage. |
| **Mesure** (*bar*) | Un groupe de **4 temps**. | « 1-2-3-4 » = une mesure. |
| **Phrase** | En général **8 mesures** (≈ 15 s à 126 BPM). La musique de club change souvent de section toutes les 8, 16 ou 32 mesures. | Comme une phrase d'écriture : elle a un début et une fin. |
| **Kick** | La **grosse caisse**, le « boum » régulier de la house et de la techno. | Le cœur du morceau. |
| **Hi-hat** (charleston) | Les petits « tss tss » aigus entre les kicks. | Le « grain » du rythme. |
| **Snare / clap** | La **caisse claire** : le « clac » sur les temps 2 et 4. | Les roulements de caisse claire annoncent souvent une montée. |
| **Basse** (*bass*) | Le grave qui ronronne sous le kick. | Quand elle tombe, c'est souvent un break. |
| **Densité** | « Combien de coups par temps » : beaucoup de notes ou de drums = son *plein*. | Un morceau chargé ≠ un morceau aéré. |

## 2. La structure d'un morceau

| Mot | Ça veut dire | Ce que le montage en fait |
|---|---|---|
| **Intro / outro** | Début / fin du morceau, souvent sans kick franc. | Images lentes et larges. |
| **Couplet** | Le kick tourne, mais le morceau n'est pas au maximum. | Peu d'écrans (1 à 2), séjours plus longs. |
| **Montée** (*build-up*) | Le son monte (aigus, caisse claire qui roule) avant le drop. | Accélérer : rafale, plus d'écrans. |
| **Drop** | Le moment où tout revient en force après la tension. | Plusieurs écrans, montage plus rapide. |
| **Break** | Une pause : le **kick disparaît** (et le grave tombe). | **Une seule image**, qui joue longtemps. |
| **Refrain** | Dans la page : le moment le plus « plein » du morceau. | Plus d'écrans (2 à 3). |

> 💡 La règle de reconnaissance « kick ou pas kick » est très simple : *plus de 2 kicks à la suite = drop ; moins de 2 = break* (puis affinée pour ne pas se tromper sur un kick raté).

## 3. Les images : le vocabulaire VJ

| Mot | Ça veut dire |
|---|---|
| **VJ** | Vidéo-jockey : celui qui « mixe » des images en direct, comme un DJ le fait avec le son. |
| **Resolume Arena** | Le logiciel de VJ de référence. Il fonctionne avec des **clips** rangés dans une **grille de colonnes**. D'autres : Modul8, VDMX, TouchDesigner. |
| **Loop** | Une courte vidéo qui boucle (de 2 s à 100 s ici). |
| **Plan** | Un « morceau » de film entre deux coupes. Une loop peut contenir plusieurs plans. |
| **Coupe** | Le moment où l'image change de plan. |
| **Couche** (*layer*) / **écran** | Une « piste » vidéo. Plusieurs couches empilées = plusieurs images en même temps. Le projet en utilise **3 maximum**. |
| **Opacité** | La transparence d'une couche (0 % invisible, 100 % pleine). Alterner 100 % / 0 % sur deux couches = l'image « saute » de l'une à l'autre. |
| **Fusion** (*blend*) | La façon de mélanger deux couches. **Alpha** = l'image du dessus recouvre l'autre. **Add** (« 50 Add ») = les couleurs **s'additionnent** : ça éclaircit, ça fait « lumière sur lumière ». |
| **Repère** (*cue*) | Un point d'entrée dans une loop. On « saute » sur un repère pour ne pas toujours repartir du début. |
| **Masque** | Une loop sur fond noir qu'on pose **par-dessus** une autre (effet : une forme qui révèle l'image dessous). |
| **One-shot** | Une loop jouée **une seule fois**, sans boucler (souvent juste avant un break ou un drop). |
| **Rafale** (*burst*) | Les images se partagent le temps : une nouvelle image à **chaque temps**. Pour une grosse montée. |
| **Strobe** | Bascule très rapide entre deux images (2 fois par temps). Un flash. |
| **Respiration** | Une image qui reste en place **plusieurs coups** au lieu de changer à chaque temps. Ça évite l'effet « métronome ». |
| **Vitesse** | Un tag : loop **lente**, **moyenne** ou **rapide** (selon la fréquence de ses coupes et de ses mouvements). |
| **Thème** | Le « dossier » d'une loop : films, humains, glitch, street, space… |
| **Composition / colonne / timeline** | L'ordre des loops dans la grille de Resolume. Ici il est **classé comme une histoire** (du plus humain au plus abstrait) : deux colonnes voisines se ressemblent. |
| **Chapitre / palier** | Les 4 grandes familles de la composition : **humain → figuratif → texture → abstrait**. |
| **Mood** | L'ambiance d'une loop : **house** (positif), **techno** (énervé) ou « les deux ». Le bouton « Tout » = aucun filtre. |
| **Famille de styles** | Un style musical plus fin (ex. « hip hop, rap », « acid », « ambiant »). Chaque famille a un mood. |
| **Tag** | Une étiquette `famille:valeur`, par exemple `couleur:désaturé` ou `sujet:personne`. Deux loops qui partagent un tag « se parlent ». |
| **Vivier** (*pool*) | La liste des loops *autorisées* à jouer à un moment donné (après filtres de mood, style, mode, tags…). |
| **Old / NSFW** | Loops marquées « vieilles » ou pour adultes : tenues à l'écart du montage normal. |

## 4. Les 4 modes de montage

| Mode | En une phrase | Déclencheur |
|---|---|---|
| **Drop** | Montage normal : plusieurs images qui alternent. | Le kick est là, le morceau est lancé. |
| **Break** | **Une** image, qui joue d'un trait, longtemps. | Le kick disparaît et le grave tombe. |
| **Suspension** | Images **presque immobiles** (très peu de mouvement), comme une respiration. | Le kick manque en plein drop (même 2 temps). |
| **Hyper** | Images **rapides, intenses** (le côté « hardcore »). | Le son est « plein » : beaucoup de notes ou de drums. Jamais sur un morceau lent. |

## 5. Les mots de l'algorithme

| Mot | Ça veut dire |
|---|---|
| **Autopilot** | Le mode où le programme joue seul, sans main humaine. |
| **Séjour** | Le temps qu'une image reste à l'écran avant de céder la place. Ici ≈ **4 secondes**. |
| **Loop dominante** | « Le personnage principal » d'une séquence : elle revient et joue des plans **longs**. |
| **Satellites** | Les autres loops, qui **tournent autour** de la dominante en plans courts. |
| **Aller-retour** | Faire revenir dans la même séquence une loop déjà passée, pour créer une histoire. |
| **Non-retour** | Ne **pas** rejouer une loop tant que toutes les autres du vivier ne sont pas passées. |
| **Neuve / retour** | Une loop « neuve » n'a pas été vue depuis longtemps ; un « retour » en est une qu'on a vue il y a moins de 10 min. |
| **Plafond** | Une limite maximale (ex. un même film ne peut pas prendre plus de 3 loops par demi-heure). |
| **Voisinage** | Choisir la loop suivante parmi les **10 colonnes voisines**, avec 1 chance sur 5 de sauter ailleurs. |
| **Lien (thème / tags)** | Deux logiques qui alternent : *changer de thème* ou *garder au moins un tag en commun*. |
| **Paire de montage** | Deux loops que l'auteur a déjà enchaînées lui-même dans ses clips : elles reviennent de temps en temps ensemble. |
| **Repli** (*fallback*) | Quand un filtre ne laisse que trop peu de loops, on le **relâche** plutôt que de rejouer toujours les mêmes images. |

## 6. Le vibe coding, c'est quoi ?

**Vibe coding** = construire un programme en **décrivant ce qu'on veut avec ses mots** à une IA, au lieu d'écrire le code soi-même. On parle, on regarde le résultat, on corrige, on recommence.

| Mot | Ça veut dire |
|---|---|
| **Prompt** | Le message qu'on envoie à l'IA. Ici : des phrases de VJ, souvent à l'oral (« ça change trop vite », « mets-moi plus de suspensions »). |
| **Consigne** | Une règle dictée dans un prompt. |
| **Codex (V1 → V88)** | Le **carnet de règles** du projet : chaque règle validée reçoit un numéro (V68, V72…). Un « V » = une décision. |
| **Page des choix** | Une page où l'IA a proposé des options (A1, B2…) et où l'auteur a tranché. |
| **« Proposition, à valider »** | Une règle que l'IA a proposée et que l'auteur n'a pas encore confirmée : les chiffres sont là pour être corrigés. |
| **Constante nommée** | Un chiffre réglable écrit en haut d'un fichier, avec un nom clair : `HYPER_REPOS_MESURES = 32`. Pour changer la règle, on change le chiffre. |
| **Banc / mesure** | Un test sur un vrai morceau ou un vrai live, pour vérifier qu'une règle fait bien ce qu'on croit. |
| **Dette** (*tech debt*) | Un raccourci connu : « ça marche, mais il faudra le ranger un jour ». |
| **Dashboard** | L'application privée de l'auteur pour piloter Resolume en live. Le site en reprend le cerveau. |
| **Pyodide** | Une technologie qui fait tourner du **Python dans un navigateur web**. |
| **Manifeste** | Le fichier `manifest.json` du site : la fiche d'identité de toutes les loops (nom, style, tags, fichiers…). |
| **R2** | Le stockage cloud (Cloudflare) où sont les vidéos. |

## 7. Lire une règle, ligne par ligne

Chaque règle d'After TV suit presque toujours le même chemin :

```
1. LA PHRASE DU VJ        →  ce qu'il a ressenti ou voulu (en mots simples)
2. LE NUMÉRO DE CODEX      →  V68, V72… : la décision est gardée
3. LA RÈGLE EN CLAIR       →  une phrase précise, avec un chiffre
4. LA CONSTANTE            →  le chiffre, dans le code, réglable
5. LA PREUVE               →  une mesure sur un vrai set qui justifie le chiffre
```

**Exemple 1 — « Les images changent trop vite » (règle V68, la loop dominante)**

| Étape | Contenu |
|---|---|
| Phrase du VJ | Les loops s'enchaînent trop vite, on n'a pas le temps de raconter quelque chose ; chaque séquence a besoin d'un personnage principal. |
| Numéro | **V68** |
| Règle en clair | La première loop de la séquence est la **dominante** : elle joue des plans longs ; les autres passent autour en plans courts. |
| Constantes | `DOMINANTE_BLOC_MESURES = 4` (un bloc de 4 mesures) · `SATELLITE_TEMPS = 2` (un satellite dure 2 temps) |
| Effet | Dans un bloc de 4 mesures : la dominante ≈ 3,5 mesures, un satellite 2 temps. |
| Ce que tu peux faire | Sur ton logiciel : une loop qui reste 4 mesures, puis un éclair de 2 temps d'une autre, puis retour. |

**Exemple 2 — « Hyper, pas trop souvent » (règle V56)**

| Étape | Contenu |
|---|---|
| Phrase du VJ | L'hyper doit se sentir quand il y a plein de notes ou de drums ; une par minute, c'était trop intense. |
| Constantes | `HYPER_MESURES = 4` (dure 4 mesures) · `HYPER_REPOS_MESURES = 32` (puis 32 mesures de repos) |
| Preuve | Mesure : 7 hypers en 8,7 minutes avant réglage. |
| Ce que tu peux faire | Un « effet fort » = court (4 mesures) et rare (1 fois toutes les ~40 mesures). |

**Exemple 3 — « Les moins vues d'abord » (règles R1 à R3, V86 à V88)**

| Étape | Contenu |
|---|---|
| Problème mesuré | Le catalogue de 818 loops se « consommait » en 45 minutes à ~10 loops neuves par minute. |
| Règle | Au plus **3 loops neuves par minute** : au-delà, on fait revenir une loop récente. |
| Résultat visé | À 5 par minute, le catalogue durerait 1 h 30 ; à 3, plus de deux heures. |
| Ce que tu peux faire | Prépare une sélection de 40 loops pour un set de 20 min plutôt que d'en balancer 200. |

> 🔎 **Astuce de lecture** : quand une règle donne un chiffre en *mesures*, convertis-le en secondes avec la calculette plus bas pour « sentir » la durée.

## 8. Écrire ton propre prompt de VJ

Les prompts de l'auteur marchent bien parce qu'ils sont **perceptifs** (ce qu'il voit ou entend) et **concrets**. Une bonne recette :

```
1. CE QUE JE VOIS / ENTENDS   « Pendant les breaks, les images changent trop souvent. »
2. CE QUE JE VEUX             « Je veux une seule image qui reste longtemps. »
3. UN CHIFFRE OU UN EXEMPLE   « Au moins 8 mesures, comme sur tel morceau. »
4. LES EXCEPTIONS             « Sauf si le break dure moins de 4 mesures. »
5. COMMENT VÉRIFIER           « Fais-moi voir pourquoi tu as changé d'image. »
```

| ❌ Trop vague | ✅ Mieux |
|---|---|
| « Fais plus de variété. » | « Utilise aussi la suspension et l'hyper : je ne les vois jamais passer. » |
| « C'est trop rapide. » | « À 90 BPM, ne mets que des loops lentes ; pas de plan plus court qu'un temps. » |
| « Fais quelque chose de cool au drop. » | « Au drop, montre un visage 7 fois sur 10 : ça relance l'attention. » |
| « Ça se répète. » | « Ne rejoue pas une loop tant que les autres du vivier ne sont pas passées. » |

Pense aussi à **demander les raisons** : l'une des meilleures idées du projet est une console qui affiche *pourquoi* chaque loop est entrée (« tag en commun : couleur:désaturé », « paire de montage », « loop dominante »). Quand tu codes à l'oreille avec une IA, exige-lui cette traçabilité.

## 9. Calculette BPM → secondes

Pour traduire « 8 mesures » ou « 2 temps » en secondes. (Formule : 1 temps = 60 ÷ BPM ; 1 mesure = 4 temps.)

| BPM | 1 temps | 1 mesure | 2 mesures | 8 mesures | 16 mesures |
|---|---|---|---|---|---|
| 90 (lent, hip-hop) | 0,67 s | 2,7 s | 5,3 s | 21,3 s | 42,7 s |
| 126 (house, le défaut du site) | 0,48 s | 1,9 s | 3,8 s | 15,2 s | 30,5 s |
| 135 (techno) | 0,44 s | 1,8 s | 3,6 s | 14,2 s | 28,4 s |

> Le « séjour » de 4 s d'After TV, c'est donc environ **2 mesures** à 126 BPM : une nouvelle loop toutes les 2 mesures.
