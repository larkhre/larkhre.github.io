# Larkhré

*Mossi sef raanné* : « la langue de la machine », en soninké. Et *larkhré*, c'est la bouche.
Le langage pour apprendre à coder en français, avec des erreurs qui t'expliquent quoi corriger.

```
laz nom = "Awa"

fonk saluer(qui) {
    rend "Bonjour " + qui + " !"
}

pou i dan 1..3 {
    vox(saluer(nom))
}
```

![tests](https://github.com/larkhre/larkhre.github.io/actions/workflows/tests.yml/badge.svg)

## Essayer

**Dans le navigateur, sans rien installer :** [larkhre.github.io/code](https://larkhre.github.io/code/)
(marche aussi sur téléphone, et hors ligne une fois ouvert).

**Sur ton ordinateur (Python 3) :**

```bash
pip install larkhre
larkhre mon_programme.laz     # exécuter un fichier
larkhre                       # mode interactif
```

Sans pip : `python3 larkhre.py exemples/demo.laz`.

## Pourquoi Larkhré

- **Les erreurs sont expliquées en français**, avec le « film » des dernières valeurs avant le plantage.
- **Des mots-clés écrits comme on parle** : `laz` (variable), `vox` (afficher), `kan` (quand),
  `tanke` (tant que), `pou … dan` (pour … dans), `fonk` (fonction), `walu` (rien).
- **`ralenti()`** montre le programme s'exécuter ligne par ligne, variables visibles.
- **Tes langues** : `#langue: anglais`, `#langue: francais` (académique), et des packs en bambara et en wolof.
- **Une passerelle vers Python** : `larkhre --traduire prog.laz` produit du Python lisible.

## Le langage en 30 secondes

| Larkhré | Signification |
|---|---|
| `laz x = 5` | déclarer une variable |
| `vox("salut")` | afficher |
| `demand("Ton nom ? ")` | saisie clavier (renvoie un texte) |
| `kan … { } sinon { }` | si / sinon |
| `tanke … { }` | tant que |
| `pou i dan 1..10 { }` | boucle pour |
| `fonk f(x) { rend x }` | fonction et retour |
| `kase` / `swiv` | break / continue |
| `vrai` / `faux` / `walu` | true / false / null |
| `et` / `ou` / `non` | and / or / not |
| `klas … herite …` | classes et héritage |
| `vox("Salut {nom}")` | interpolation |
| `essaie { } rattrape err { }` | gestion d'erreurs |
| `garde score = 0` | variable qui se souvient entre deux exécutions |

Le manuel complet : [GUIDE_LARKHRE.md](GUIDE_LARKHRE.md). L'historique : [CHANGELOG.md](CHANGELOG.md).

## Apprendre

- **L'École**, dans le playground : 12 leçons avec vérification automatique.
- **Le livre** *Apprends à coder de zéro* : 14 chapitres, exercices corrigés, 3 projets.
  Tous ses exemples sont vérifiés automatiquement dans [`tests/`](tests/).

## Pour les développeurs

- **Deux moteurs** : `larkhre.py` (Python, zéro dépendance) et le moteur JavaScript du
  playground (`docs/code/index.html`), publié sur npm : `npm install larkhre`.
- **Tests** : `python3 tests/run_tests.py` lance chaque programme sur les deux moteurs et compare
  leur sortie. GitHub les relance à chaque modification.
- **React** : le composant `<LarkhrePlayground />` dans [`react/`](react/).
- **Agents IA** : le serveur MCP `larkhre-mcp` dans [`mcp/`](mcp/), et la spécification pour IA
  dans [LARKHRE_POUR_IA.md](LARKHRE_POUR_IA.md).

## English

Larkhré ("the mouth" in Soninke; *mossi sef raanné*, "the language spoken by the machine") is a beginner-friendly
programming language with French keywords and error messages that explain what to fix.
Curly braces, no semicolons. Try it in the browser at
[larkhre.github.io/code](https://larkhre.github.io/code/) or `pip install larkhre`.
Two engines (Python and JavaScript) are checked against the same test suite on every commit.

## Licence

MIT — libre et gratuit, pour tout le monde. Créé par Ladji Doucaré, 2026.
Anciennement LAZARUS.
