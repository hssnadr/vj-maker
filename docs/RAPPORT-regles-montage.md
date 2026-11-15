# After TV — rapport sur les règles qui pilotent les vidéos

*Source : le code public servi par https://odcstudio.fr/after-tv/ (page, scripts JS, manifeste, et les 22 modules Python chargés dans le navigateur via Pyodide, ~9 200 lignes). Relevé le 2026-11-15.*

## 1. En bref

Le montage vidéo d'After TV n'est pas du hasard : c'est un **moteur de règles** qui écoute le son, comprend où en est le morceau (break, drop, montée…) et choisit à chaque instant quelles loops (parmi 818) jouent, combien d'écrans, combien de temps, et avec quel effet.

Ces règles viennent presque toutes de **consignes dictées en langage naturel** par l'auteur, « Oscar » (VJ Rien), à un assistant de code, par sessions successives entre le **2026-09-08 et le 2026-11-14**. Le code en garde la trace de trois façons :

- des **citations verbatim** entre « guillemets » avec leur date (≈ 220 mentions d'« Oscar » dans le code) ;
- un **codex numéroté V1 → V88** (une règle = un numéro ; ex. « V68 : chaque séquence a une loop dominante ») ;
- une **« page des choix »** (2026-11-12) où Oscar a tranché des propositions (A1, D2…), et des mentions « PROPOSITION, à valider par Oscar » pour les règles pas encore validées.

Deux nuances utiles : certains chiffres sont **dictés** (« trois fois », « 2 beats », seuil de mouvement 1,5), d'autres **mesurés** sur ses vrais sets (Justice, Sawf…) puis ajustés ; et beaucoup de règles sont des **freins anti-répétition** ajoutés après avoir mesuré des défauts en direct.

## 2. La chaîne de décision

```
son (ordinateur / micro / radio Intergalactic FM)
  → oreille : tempo, kicks, grave/médium/aigu, genre (YAMNet), motifs, densité, groove
  → structure : break / drop / montée / refrain / couplet…
  → live.py (vivier + règles d'enchaînement) + outils_auto.py (outils d'autopilot)
  → pilote_web.py : un pas par temps -> miroir_web -> couches (1 à 3) avec opacité / fusion
  → la page (index.html) : lit les .mp4, SD ou HD, en fondu
```

Si le moteur ne charge pas (ou sans son), `montage.js` joue une **version de veille** réduite : deux loops liées qui alternent sur les temps. Le « Tout / House / Techno » du site n'est qu'un filtre du vivier (cf. §4.1).

## 3. L'écoute : ce qui déclenche les changements

| Règle | Valeur / formulation | Origine |
|---|---|---|
| **Break / drop** | « Si y'a plus de 2 kicks à la suite c'est un drop, moins de 2 kicks c'est un break » ; « la basse décide, le kick confirme » | V53 (nuit du 2026-11-12), V-« 2 beats » du 2026-09-19 : « le changement se fait sur 2 beats » |
| Pas de faux break | un kick raté ne fait pas un break : deux temps vides **et** grave en chute | mesuré sur 39 min de Justice |
| Parties du morceau | intro, couplet, montée, refrain, break, outro (mesurées au volume, pas au chant) | demande 2026-11-12 : « ça nous aiderait énormément » |
| Réaction aux ruptures | une rupture nette fait réagir tout de suite, sans attendre la grille | V71 |
| **Pas de son = écran noir « After TV »** après 4 s | fondu vers le noir, images de retour avec le son | V74 : « quand y'a pas de son tu dois mettre un écran noir avec écrit after tv » |
| Écoute fine → montage | un refrain qui revient ramène ses loops ; un riff qui revient aussi ; le drop annoncé prépare ses loops une mesure avant ; le rythme qui change (4/4 → cassé) change la loop dominante | 2026-11-14 : « fais tout, et montre-moi petit à petit » |
| Source par défaut | son de l'ordinateur ; micro si rien ne sort ; sur téléphone, micro par défaut | V45 ; 2026-11-14 |

## 4. Quelles loops ont le droit de jouer (le vivier)

1. **Mood** (le sélecteur du site) : « tout » = aucun filtre ; une loop non jugée vaut « les deux » ; **les loops NSFW sont forcément techno** (2026-09-25) ; une loop « les deux » prend l'humeur de son dossier (« toutes les loops nonne c'est techno », 2026-11-14).
2. **Styles musicaux** (2026-11-12) : 14 familles (house, disco/funk/soul, hip-hop, pop/rock/psyché → *positif = house* ; techno, trance, acid, hard techno, dub, mélodique, breaks/dnb → *énervé = techno*, V76). Ambiant/expérimental = « que des loops de house très lentes ». La famille est un **accent** (la loop dominante vient d'elle), pas un vivier : « une dominante loop rock, mais on peut garder les vidéos de House ». Si moins de 8 loops de la famille, on revient au mood (anti-ressassement).
3. **Exclusions** du montage normal : loops `old` (vieilles), `one_shot`, `mask` (masques posés par-dessus). Les one-shots et suspensions peuvent quand même passer environ 1 fois sur 10 « de temps en temps dans une séquence » (V81, 2026-11-14).
4. **Tout le catalogue joue** (V80, 2026-11-14 : « loops space : il faut les intégrer ») ; le pool s'est ouvert par paliers : 150 → 250 → 350 → 500 (2026-09-19/23) → tout (2026-09-25 : « ouvrir tous les loops à la lecture »).
5. **Vitesse suit le tempo** (V66) : « quand on a 91 bpm tu dois mettre des vidéos plus lentes ! » → sous 100 BPM : loops lentes d'abord, jamais de rapide ; jusqu'à 125 : tout sauf plans très courts ; au-dessus : tout. Pas d'« hyper » sous 100 BPM.
6. **Loops courtes** : moins de 5 s = jamais un break ni une suspension (« toutes les loops de moins de cinq secondes c'est dans rapide », 2026-09-09).

## 5. Comment les loops s'enchaînent

| Règle | Détail | Origine |
|---|---|---|
| **Séjour de 4 s** | à chaque pas, la plus ancienne loop sort, une nouvelle entre | V41, V42 |
| 2 loops alternent sur les temps | opacité 1/0 en alternance, fusion « Alpha » | V8 |
| **3 écrans maximum** | « retirer le 4ᵉ écran partout » (2026-10-10) ; 3 pistes en ligne (2026-11-14) | V6, V7 |
| **Un thème par écran** | deux vidéos du même dossier en même temps = « la même image deux fois » | 2026-09-09 |
| **Tag en commun** | la nouvelle loop partage ≥ 1 tag avec celle qui reste ; les tags rares comptent plus que les courants | V46 |
| Alternance des deux logiques | thème / tags, toutes les 180 s (« passer d'une condition à l'autre dans un range de 3 minutes ») | V47, 2026-11-11 |
| **Voisinage sur la timeline** | on tire dans ±10 colonnes de la composition ; 1 fois sur 5 on saute ailleurs ; 60 % de chance de rester dans la même « famille de composition » | V44, 2026-09-09/24 |
| **Paires de montage** | 40 paires que l'auteur a lui-même enchaînées dans ses clips ; jamais avant 10 min de live, ≥ 5 min d'écart, 1/6 de chance, jamais deux de suite. *Actives dans la version de veille (`montage.js`) ; le moteur Pyodide les a désactivées (`paires = []`, noté « DETTE » : le manifeste n'a pas les chemins de fichiers pour les reconnaître) — cf. rapport 2* | V52, V83 (« au début 1 fois sur 2… et si le live dure longtemps tu vas le faire moins ») |
| **Préférences de ses vrais montages** | pour chaque famille de tags, on tire la suivante en proportion de ce qu'il garde vs change (le sujet : gardé 21 % chez lui contre 8 % au hasard) | V84 (`regles_montage.json`, 328 paires mesurées) |

## 6. La narration (rythme et « histoire »)

- **Loop dominante** (V68) — la raison d'être du réglage : *« les loops changent trop vite, on n'a pas le temps d'avoir une puissance narrative… chaque séquence doit avoir une loop dominante, sinon c'est juste un catalogue de loops mises bout à bout »*. La première loop joue des plans longs (3,5 mesures sur 4) ; les autres passent autour en plans de 2 temps.
- **Allers-retours** (V69) : « tu dois aussi bien faire des allers-retours entre les loops pour créer une histoire narrative ». 2 satellites par séquence ; la loop qui sort laisse la place à une loop déjà passée dans la séquence.
- **Plans d'une loop** (V65, « règle d'or ») : si une loop contient plusieurs plans, elle peut tenir **seule** une phrase de 8 mesures (un plan par mesure) au lieu de changer de vidéo sur le BPM.
- **Chapitres / dérive** (2026-09-09) : 4 paliers — humain → figuratif → texture → abstrait. À partir du drop, le montage dérive vers l'abstrait puis **revient d'un coup aux visages après 16 mesures** ; jamais plus de 32 mesures sans visage ; un visage tient 16 mesures ; un drop montre des visages 70 % du temps.
- **Respiration** (V60) : une image peut tenir plusieurs coups (house : 2 ; techno : 1 ; doublé après 16 mesures) ; 25 % du temps une image reste en place plusieurs coups pour casser l'alternance « trop binaire ».

## 7. Les modes et les outils de l'autopilot

| Mode / outil | Règle | Origine |
|---|---|---|
| **Break** | UNE seule image (« un break, c'est un solo »), qui joue d'un trait sans saut de repère ; ouvre à 2 écrans après 16 mesures | 2026-09-08, 09-14 |
| **Long break** | garde sa loop longtemps : « n'hésite pas à laisser des loops de break longtemps sans changer de loop si tu sens que c'est une longue pause » | V72 |
| **Suspension** | loops presque statiques (mouvement ≤ 1,5 sur 100 — « le chiffre est d'Oscar, pas une déduction ») ; jouée **dès que le kick manque en plein drop**, même 2 temps seulement, plus souvent | V55, V82 (« suspension de 2 beats ») |
| **Hyper** | loops hardcores/roses ; part quand le son est *plein* (« plein de notes ou plein de drums »), 4 mesures puis repos de 32 (« une par minute était trop intense ») ; jamais dans un break | V56, V85 |
| **Écrans** (1/2/3) | tirés toutes les 8 mesures de drop ; après 16 mesures jamais un seul écran | V57, 2026-09-14 |
| **Rafale** | pour une grosse montée : quand charleston/caisse claire *montent*, 2 dernières mesures de chaque phrase de 8 | V58 |
| **Déclencheur** | le montage suit le hi-hat quand il est franc, 2 mesures au plus puis retour au kick 12 mesures (« pas trop longtemps… sinon ça va être trop intense ») | V59, V70 |
| **Masque / dosage** | 1 passage à 2 écrans sur 3 en fusion additive (« + »), masque par-dessus à 70 % | V62 |
| **Strobe** | dernière mesure de chaque rafale du drop, 2 bascules par temps (« l'allumer », en sachant que la page est publique) | V63 |
| **One-shot** | une loop de suspension jouée UNE fois, juste avant un break/drop, seulement si le changement est quasi certain (≥ 32 mesures, confiance 0,6, ≤ 4 mesures) | 2026-09-23 |
| Datamosh « DM… » | « il faut les jouer beaucoup moins, c'est un effet trop fort » → ≤ 1 sur 12 loops tirées | 2026-11-14 |

## 8. Les freins anti-répétition (ajoutés après mesures)

- **Non-retour** (V21) : une loop passée ne revient pas avant que le reste de son vivier soit passé ; mémoire de 40 loops sur la page de veille. Mesuré : 14 colonnes sur 127 ne sortaient *jamais* pendant que d'autres passaient 32 fois (2026-09-09).
- **Un mode reprend sa loop 3 fois au plus par morceau** (V77, « Oui, 3 fois » — la suspension reprenait la même loop 14 fois en 18 min).
- **R1 (V86)** : au plus **3 loops neuves par minute** (2 en break) ; au-delà, un *retour* d'une loop passée il y a < 10 min (mais absente depuis ≥ 30 s). Motif mesuré : « ~10 neuves par minute, le catalogue fait en 45 min ; à 5 par minute il tient 1 h 30 ».
- **R2 (V87)** : parmi les candidates, favoriser celles qui ont le moins passé de temps à l'écran (tolérance 15 s).
- **R3 (V88)** : un même **film** fait entrer au plus **3 loops par 30 min** et ne dépasse pas 2 % de l'écran (le dossier « nonnes » avait pris 13 % de l'écran en 20 min).

## 9. Règles d'interface et de produit (la page)

« Toujours automatique » (pas de pilotage manuel côté public) ; **House par défaut** ; textes en **anglais** (« mets tout en anglais ») ; trois radios Intergalactic FM avec **nom complet** (« écris bien Cybernetic… et pas juste CBS ») ; **HD auto** (SD sinon), bouton de qualité demandé le 2026-11-12 ; plein écran sorti du panneau ; « attention aux panels qui se superposent » ; vidéo figée sur la 1ʳᵉ frame = bug à éviter (2026-11-12) ; **console de debug pédagogique** « entendu → déduit → effet à l'écran → règle d'Oscar » (2026-11-14) ; nouvelle version qui se recharge seule ; crédit « a project by @vj_rien_ and @enjoy.dot » ; audience sans cookie ni identifiant personnel.

## 10. Chronologie des « sessions de dictée » visibles dans le code

| Date | Thèmes |
|---|---|
| 2026-09-08/09 | break = 1 image, repères/sauts, superposition par phases, voisinage, chapitres, dérive 16 mesures, un thème par écran, vitesse < 5 s |
| 2026-09-14/17/19 | horizon 8 mesures, 2 écrans après 16, non-retour par mode, « blend en break aussi », « la moitié de l'échantillon n'est pas jouée » |
| 2026-09-23/25 | one-shot, vieilles loops, loops étoilées, masques, NSFW = techno, ouverture de tout le pool |
| 2026-10-10 | 3 écrans maximum (V6) |
| 2026-11-09 | essai de reconnaissance de morceaux (AudD, coût maîtrisé) |
| 2026-11-11 | alternance thème/tags (V47), son de l'ordinateur par défaut (V45) |
| **2026-11-12** | grosse nuit : codex V51 → V77 (break/drop par les kicks, dominante, aller-retours, plans, outils auto, « page des choix », écran noir sans son, familles de styles) |
| 2026-11-14 | V80–V88 : space intégré, suspensions de 2 temps, quotas R1–R3, écoute fine « fais tout », console pédagogique, documentation interactive, HD auto |

## 11. Lecture critique

- **Tension centrale** : le tempo de 4 s (V41/V42) donne un défilé trop rapide ; la réponse d'Oscar (« pas de puissance narrative ») produit toute la couche dominante / allers-retours / plans / quotas. Le montage est donc un compromis entre *variété* (voir tout le catalogue) et *récit* (garder une loop).
- **Statut des règles** : les numéros V sont des règles « validées » ; les outils d'autopilot V55–V63 sont explicitement des **propositions** dont « les chiffres sont en tête de fichier pour qu'il les corrige ». Le code signale aussi des « DETTES » (fonctions recopiées depuis `app.py`).
- **Limite de ce rapport** : tous les fichiers ont été lus, mais `live.py` (2 042 lignes) et `structure.py` (1 010) ont été relevés par leurs constantes et commentaires de règles, pas ligne à ligne ; le détail des algorithmes d'écoute (kick, tempo) n'est pas analysé. Le codex source (`docs/CODEX-VJ.md`) n'est pas public : seules ~9 règles y sont recopiées dans la page (V45, V51, V52, V59, V68, V71, V72, V74, V82).
- **Lien avec l'outil de téléchargement** : le manifeste que le scraper récupère contient exactement les champs que ces règles consomment — `mood`, `styles`, `vitesse`, `plans`, `colonne` (ordre de la timeline), `theme`, `tags`, `old`/`one_shot`/`mask`. `catalogue.csv` permet donc de reconstituer les viviers ci-dessus.
