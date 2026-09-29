# Historique des versions

## 11.2 — Le téléphone d'abord (septembre 2026)
- **`{moi.nom}` dans les textes** : l'interpolation accepte maintenant les champs d'un objet, et même
  `{joueur.arme.nom}`. Un chemin inconnu reste affiché tel quel, comme une variable inconnue.
  Identique dans le moteur Python, le playground et la traduction vers Python.
- **Barre de symboles sur téléphone** : quand on écrit dans le cahier sur un écran tactile, une barre
  apparaît au-dessus du clavier avec `" ( ) { } [ ] = +`, une tabulation et deux flèches pour
  déplacer le curseur.
- Tests : 48 programmes vérifiés sur les deux moteurs.

## 11.1 — Larkhré (septembre 2026)
- **Nouveau nom : LAZARUS devient Larkhré** (*mosi larkhré* : « la langue de la machine », en soninké).
  Les programmes existants marchent sans changement ; `#langue: lazarus` reste accepté.
- Paquets : `pip install larkhre`, `npm install larkhre`, serveur MCP `larkhre-mcp`.
- Site : page d'accueil sur [larkhre.github.io](https://larkhre.github.io/), playground sur
  [larkhre.github.io/code](https://larkhre.github.io/code/). L'ancienne adresse redirige et transmet
  la progression de l'École.
- Le moteur Python arrête désormais les boucles infinies, comme le playground.
- Tests : 47 programmes du livre vérifiés sur les deux moteurs à chaque modification (`tests/`).

## Versions précédentes (sous le nom LAZARUS)
- **11.0** — `#langue: python` : du vrai Python (sous-ensemble lycée) avec les erreurs expliquées en français.
- **10.0** — mode quantique : `qubits`, `superpose`, `intrique`, `mesure`.
- **9.0** — L'École (12 leçons dans le playground) ; `ecoute()` : le programme entend la voix.
- **8.0** — `dis()` : le programme parle ; appli installable hors ligne ; partage par lien.
- **7.0 / 7.1** — mode interface (boutons, champs) ; pack français académique.
- **6.0** — jeux en temps réel (`chaque_image`, clavier, sons) ; moteur npm et composant React.
- **5.0** — `garde` (variables qui se souviennent), `ralenti()`, mots-clés multilingues.
- **4.0** — interpolation `{nom}`, `essaie` / `rattrape`, traduction vers Python.
- **3.0 / 3.1** — couleurs, raccourcis `+=`, mode dessin et export SVG.
- **2.0** — classes (`klas`, `herite`), dictionnaires, modules, fichiers.
- **1.0** — le langage : `laz`, `vox`, `kan`, `tanke`, `pou … dan`, `fonk`.
