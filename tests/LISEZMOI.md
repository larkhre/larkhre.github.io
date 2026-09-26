# Les tests

Chaque fichier de `programmes/` est un programme tiré du livre *Apprends à coder de zéro*.
Le script les exécute sur **les deux moteurs** — l'interpréteur Python (`pip install`)
et le moteur JavaScript du playground (`docs/`) — et vérifie que chacun affiche
exactement la sortie attendue.

```
python3 tests/run_tests.py            # lancer les tests (Python 3 et Node.js requis)
python3 tests/run_tests.py --generer  # créer le .attendu d'un nouveau programme
```

- `nom.laz` : le programme ;
- `nom.in` (facultatif) : ce que l'utilisateur tape au clavier, une réponse par ligne ;
- `nom.attendu` : ce que les deux moteurs doivent afficher.

Pour ajouter un test : écris `nom.laz` (et `nom.in` si besoin), lance `--generer`.
Le fichier `.attendu` n'est créé que si les deux moteurs sont d'accord ; relis-le
avant de le garder. GitHub relance tous les tests à chaque modification
(`.github/workflows/tests.yml`).
