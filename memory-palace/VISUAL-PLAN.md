# Plan — refonte visuelle memory-palace

Objectif : le rendu 3D actuel (boîtes grises plates sur sol gris, fond nuit, brouillard) est très moyen. Refonte ciblée sur les 20 % qui font 80 % de l'impact. Pas de micro-améliorations.

Fichier principal : `memory-palace/scripts/compose-html.py` (génère le HTML autonome avec Three.js inliné).
Exemple généré pour tester : `studies/biomimetisme-locomotion-chantier/memory-palace.json` → régénérer le HTML avec le script après chaque itération.

## 1. Direction artistique « maquette d'architecte » (priorité max)

- Sol clair, palette pastel type Monument Valley / maquette carton. Palette définie **par archétype** (voir `references/palace-archetypes.md`) : chantier = sable/ambre, musée = crème/laiton, corridor = tons chauds, bibliothèque = bois/vert sombre. Fini le gris sur gris et le fond bleu nuit.
- Vraies ombres douces : `DirectionalLight` avec shadow map activée (`renderer.shadowMap.enabled`, PCFSoft), `castShadow`/`receiveShadow` sur bâtiments et sol.
- Silhouettes différenciées : toits variés (plat, pente, pignon), hauteurs variées, 1-2 détails procéduraux par archétype (grue sur chantier, fronton/colonnes sur musée, cheminées sur maisons). Plus jamais N boîtes identiques.
- Contours nets (EdgesGeometry) conservés mais adaptés à la palette claire.

## 2. Chemin de mémoire visible (cœur du skill)

- Ruban ou pointillé au sol reliant les bâtiments dans l'ordre de `path[]`.
- Gros numéro 1→N visible devant chaque entrée de bâtiment (sprite ou plaque 3D).
- La méthode des loci = le parcours ; il doit se lire d'un coup d'œil.

## 3. Bug page noire (fallback)

- Si la création du contexte WebGL échoue (throw dans `new THREE.WebGLRenderer`), la page reste entièrement noire : entourer d'un try/catch et basculer automatiquement sur le fallback iso-SVG (`#iso-map`).
- `window.FORCE_2D = true` doit réellement remplir et afficher `#iso-map` (aujourd'hui il reste vide, `display:none`).
- Le fallback iso-SVG doit hériter de la même palette claire.

## Hors scope (ne pas toucher)

Mode quiz, thèmes custom, animations avancées, optimisation mobile, refonte du panneau latéral.

## Validation

- Régénérer `studies/biomimetisme-locomotion-chantier/memory-palace.html` via `python3 memory-palace/scripts/compose-html.py studies/biomimetisme-locomotion-chantier/memory-palace.json`.
- Vérifier : plus de page noire sans WebGL (fallback visible), rendu 3D clair avec ombres, chemin numéroté visible, `bash tests/...` si des tests existent.
- Mettre à jour `references/navigation-ux.md` (les ombres ne sont plus interdites) et `palace-archetypes.md` (palettes) si nécessaire.
