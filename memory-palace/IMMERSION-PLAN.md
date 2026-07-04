# Plan immersion — memory-palace

Objectif : l'utilisateur doit pouvoir **se projeter dans le lieu**. La philosophie du palais de mémoire est de lier une abstraction à un lieu vécu par tous les sens, pas seulement par la lecture. Le rendu actuel (carte oblique propre mais abstraite) ne le permet pas. Trois priorités, rien d'autre.

## P1 — Visite guidée au sol (« mode déambulation »)

- Bouton visible « Visite guidée » sur la vue carte. Au clic : la caméra descend à hauteur d'yeux (~1.6–1.8 unités au-dessus du sol) et glisse le long du chemin de mémoire, avec easing doux (pas de téléportation).
- Elle s'arrête devant chaque locus dans l'ordre 1→N, cadré de face à distance confortable (le bâtiment remplit ~40–60 % de la hauteur du viewport).
- À chaque arrêt : le bâtiment est mis en valeur (glow / émissive légère), le panneau affiche la scène mentale du locus (voir P2).
- Navigation : boutons Précédent/Suivant + flèches clavier ←/→ ; Échap ou bouton « Vue carte » remonte à la vue oblique fit-to-bounds existante.
- Mettre à jour `references/navigation-ux.md` : la règle « no first-person movement » devient « vue carte oblique par défaut + visite guidée au sol sur rails (pas de déplacement libre) ».
- Le fallback iso-SVG n'a pas de visite 3D : il met en surbrillance le locus courant et affiche la même scène mentale, avec les mêmes boutons Précédent/Suivant.

## P2 — Scènes mentales multi-sensorielles

- `SKILL.md` (étape extraction/loci) : pour chaque locus, générer une **scène mentale** vive — une image mentale exagérée, concrète, si possible absurde ou en mouvement, qui encode le contenu — plus 2–3 accroches sensorielles (son, odeur, texture, température, mouvement).
- Schéma JSON : ajouter au locus un objet `scene` : `scene.image` (1–2 phrases, l'image mentale), `scene.senses` (liste de 2–3 chaînes préfixées du sens : « Son — … », « Odeur — … »).
- `compose-html.py` : le panneau affiche la scène mentale EN PREMIER et en grand (typo généreuse, fond légèrement teinté), le contenu factuel en dessous. Rétro-compatible : si `scene` absent, panneau actuel inchangé.
- Rédiger les scènes du study `studies/biomimetisme-locomotion-chantier/memory-palace.json` (7 loci) toi-même, vivantes et fidèles au contenu, puis régénérer le HTML.

## P3 — Environnement vivant (100 % procédural, zéro asset externe)

- Ciel en dégradé chaud + lumière dorée fin d'après-midi, ombres longues.
- Végétation et mobilier procéduraux le long du chemin : arbres simples (cône/sphère sur tronc), buissons, lampadaires ou fanions — assez pour que le lieu semble habité, pas assez pour masquer les bâtiments.
- Textures légères procédurales (canvas 2D → THREE.CanvasTexture) : grain sur le sol, lignes de bardage sur les murs. Subtil.
- Micro-animations : léger balancement du feuillage, particules de poussière discrètes dans la lumière. Doit rester fluide (60 fps sur un laptop) et ne rien casser en mode visite.
- L'iso-SVG fallback gagne au minimum le même dégradé de fond et quelques arbres SVG.

## Validation

- Les 17 tests existants (`tests/test-memory-palace.sh`) continuent de passer.
- Nouveaux tests Playwright : (a) clic « Visite guidée » → caméra à hauteur d'œil (position.y < 3) et arrêt 1 actif ; (b) Suivant × N-1 → dernier locus atteint, Échap → retour cadrage carte (position.y revient au fit) ; (c) le panneau en mode visite contient `scene.image` du locus courant ; (d) fallback iso : boutons visite présents, scène mentale affichée.
- Régénérer le study biomimétisme et produire des screenshots : vue carte, arrêt de visite n°1, fallback iso.

## Hors périmètre

Audio, VR/gyroscope, quiz, thèmes custom, mobile, déplacement libre WASD.
