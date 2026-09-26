# -*- coding: utf-8 -*-
"""Contenu du livre « Apprends à coder de zéro avec Larkhré », édition 1.1.

Chaque bloc de code est EXÉCUTÉ par le vrai moteur au moment de fabriquer le PDF :
- ecran=True  : la sortie affichée « À l'écran » est produite par le moteur ;
- entrees     : les réponses tapées au clavier (affichées après la question) ;
- avant       : du code exécuté juste avant, sans être imprimé (contexte d'un fragment) ;
- attendu     : 'ok' (aucune erreur permise) ou 'erreur' (une erreur est voulue).
Marquage dans le texte : `code`, **gras**, *italique*.
"""

PLAYGROUND = 'https://larkhre.github.io/code/'


def P(t): return ('p', t)
def H2(t): return ('h2', t)
def ASTUCE(t): return ('astuce', t)
def CODE(code, ecran=False, entrees=None, avant='', attendu='ok'):
    return ('code', dict(code=code.strip('\n'), ecran=ecran, entrees=entrees or [], avant=avant, attendu=attendu))
def EX(titre, items): return ('ex', titre, items)
def LISTE(items): return ('liste', items)


LIVRE = []

def chapitre(partie, numero, titre, blocs):
    LIVRE.append(dict(partie=partie, numero=numero, titre=titre, blocs=blocs))


# ---------------------------------------------------------------------------
chapitre('Premiers pas', None, 'Pourquoi tu vas y arriver', [
    P("Tu as déjà essayé d'apprendre à coder et abandonné ? C'est normal. La plupart des langages "
      "ont été conçus par des ingénieurs, pour des ingénieurs : en anglais, avec des messages d'erreur "
      "incompréhensibles, et une installation qui décourage avant même la première ligne."),
    P("Larkhré a été conçu pour l'inverse. Ses erreurs t'expliquent en français ce qui ne va pas. "
      "Il peut ralentir pour te montrer ton programme s'exécuter ligne par ligne, variables visibles. "
      "Il dessine. Et il fonctionne directement dans ton navigateur : rien à installer."),
    H2('Pourquoi « Larkhré » ?'),
    P("En soninké, *larkhré* veut dire la bouche, et aussi la langue. *Mosi larkhré*, c'est « la langue "
      "de la machine » : exactement ce que tu vas apprendre dans ce livre. Ce langage s'appelait "
      "auparavant LAZARUS ; si tu croises ce nom quelque part, c'est le même."),
    H2('Ton outil de travail : le playground'),
    P("Ouvre cette adresse dans n'importe quel navigateur, sur ordinateur ou sur téléphone :"),
    ('adresse', PLAYGROUND),
    P("À gauche, tu écris ton code. À droite, la console affiche le résultat. Le bouton **Exécuter** "
      "lance ton programme. C'est tout ce dont tu as besoin pour ce livre entier. Et si tu veux "
      "t'entraîner encore plus, ouvre **L'École** dans le playground : 12 leçons courtes, avec "
      "vérification automatique de tes réponses."),
    H2("La règle d'or de ce livre"),
    P("Tape chaque exemple toi-même. Ne copie-colle pas : tape. C'est en tapant qu'on mémorise, et c'est "
      "en faisant des fautes de frappe qu'on apprend à lire les erreurs, ta compétence la plus précieuse. "
      "Chaque chapitre se termine par des exercices « À toi de jouer » : fais-les tous, les solutions "
      "t'attendent à la fin du livre."),
    ASTUCE("Un chapitre par jour suffit. Dans deux semaines, tu auras créé un jeu, un quiz qui garde "
           "ton record en mémoire, et un dessin généré par ton propre code."),
])

chapitre('Premiers pas', 1, 'Ton premier programme', [
    P("Un programme, c'est une liste d'ordres que la machine exécute dans l'ordre, du haut vers le bas. "
      "Donnons-lui son premier ordre. Dans le playground, efface tout et tape :"),
    CODE('vox("Bonjour le monde !")', ecran=True),
    P("Félicitations : tu es programmeur. Décortiquons cette ligne : `vox` (comme « voix ») est la "
      "commande pour afficher à l'écran ; les parenthèses contiennent ce qu'on lui donne à afficher ; "
      "les guillemets `\"...\"` délimitent un texte. Sans eux, Larkhré croirait que `Bonjour` est une commande."),
    P("On peut afficher plusieurs choses d'un coup, séparées par des virgules, et enchaîner les ordres "
      "ligne après ligne :"),
    CODE('vox("J\'apprends à coder")\nvox("Nous sommes en", 2026)\nvox("Et ça commence bien !")', ecran=True),
    P("Remarque : `2026` n'a pas de guillemets, c'est un nombre, pas un texte. Les nombres se manient "
      "sans guillemets, et Larkhré sait calculer avec :"),
    CODE('vox("7 fois 8 égale", 7 * 8)\nvox("120 divisé par 4 égale", 120 / 4)', ecran=True),
    P("Les symboles de calcul : `+` addition, `-` soustraction, `*` multiplication, `/` division, "
      "`%` reste de la division (on y reviendra, il est plus utile qu'il n'en a l'air)."),
    P("Dernière chose : une ligne qui commence par `#` est un commentaire, une note pour toi, que la "
      "machine ignore. Prends l'habitude d'en écrire :"),
    CODE('# Mon premier programme, gardé en souvenir !\nvox("Signé : moi")'),
    EX('À toi de jouer — Exercices 1', [
        ("1.1", "Affiche ton prénom, puis ta ville, sur deux lignes."),
        ("1.2", "Fais calculer à Larkhré le nombre de minutes dans une journée (24 heures × 60 minutes), "
                "avec une phrase d'accompagnement."),
        ("1.3", "Devine avant d'exécuter : qu'affiche `vox(\"2 + 3\")` ? Et `vox(2 + 3)` ? "
                "Vérifie, et explique la différence."),
    ]),
])

chapitre('Premiers pas', 2, 'Les variables, la mémoire de ton programme', [
    P("Une variable, c'est une boîte avec une étiquette. Tu y ranges une valeur, tu lui donnes un nom, "
      "et tu peux la réutiliser partout. En Larkhré, on crée une variable avec le mot-clé `laz` :"),
    CODE('laz prenom = "Awa"\nlaz age = 16\nvox("Je m\'appelle", prenom)\nvox("J\'ai", age, "ans")', ecran=True),
    P("Lis bien la première ligne comme une phrase : « crée la boîte `prenom` et mets `\"Awa\"` dedans ». "
      "Le signe `=` ne veut pas dire « égal » comme en maths : il veut dire « mets dedans »."),
    H2('Modifier une variable'),
    P("Une fois la boîte créée, on change son contenu sans répéter `laz` :"),
    CODE('laz score = 0\nscore = 10           # nouveau contenu\n'
         'score = score + 5    # prend le contenu, ajoute 5\n'
         'score += 5           # raccourci qui fait pareil\nvox(score)', ecran=True),
    P("La ligne `score = score + 5` déroute tous les débutants, c'est normal. Lis-la de droite à gauche : "
      "calcule `score + 5` (15), puis range le résultat dans la boîte `score`. Le raccourci `+=` existe "
      "aussi en version `-=`, `*=` et `/=`."),
    H2("L'interpolation : la magie des accolades"),
    P("Écrire des phrases avec des virgules partout devient vite lourd. Larkhré a mieux : glisse ta "
      "variable entre accolades directement dans le texte :"),
    CODE('laz nom = "Moussa"\nlaz ville = "Bamako"\nvox("Salut {nom}, alors comme ça tu vis à {ville} ?")', ecran=True),
    ASTUCE("Donne toujours des noms clairs à tes variables : `prix_total` vaut mieux que `pt`. Dans six "
           "mois, ton code doit encore se lire comme une histoire. Les noms s'écrivent sans espaces ni "
           "accents : on colle les mots avec le tiret bas, comme `meilleur_score`."),
    H2('Les types de valeurs'),
    P("Tu connais déjà les textes (`\"salut\"`) et les nombres (`42`, `3.14`). Ajoutons les booléens, "
      "des valeurs qui ne peuvent être que `vrai` ou `faux`, et `walu`, qui veut dire « rien du tout » :"),
    CODE('laz majeur = vrai\nlaz pluie = faux\nlaz gagnant = walu    # personne n\'a encore gagné'),
    P("Ces valeurs deviendront essentielles au chapitre 4, quand ton programme commencera à décider."),
    EX('À toi de jouer — Exercices 2', [
        ("2.1", "Crée les variables `prenom`, `age` et `plat_prefere`, puis affiche une phrase de "
                "présentation complète avec l'interpolation `{...}`."),
        ("2.2", "Crée `argent = 1000`. Ajoute 250 avec `+=`, retire 400 avec `-=`, et affiche "
                "« Il me reste {argent} F »."),
        ("2.3", "Sans exécuter, prédis ce qu'affiche ce code, puis vérifie :"),
    ]),
    CODE('laz a = 5\nlaz b = a\na = 10\nvox(a, b)'),
])

chapitre('Premiers pas', 3, "Parler avec l'utilisateur", [
    P("Jusqu'ici, ton programme parle tout seul. Un vrai programme écoute aussi. La commande `demand` "
      "pose une question et attend une réponse au clavier :"),
    CODE('laz nom = demand("Comment tu t\'appelles ? ")\nvox("Enchanté, {nom} !")', ecran=True, entrees=['Fatou']),
    P("Ce que l'utilisateur tape est rangé dans la variable, et le programme continue. Mais attention "
      "au piège le plus célèbre du débutant : `demand` renvoie toujours un **texte**, même si on tape "
      "des chiffres."),
    CODE('laz age = demand("Ton âge ? ")\nvox(age + 1)    # « 16 » est un texte, pas un nombre !',
         ecran=True, entrees=['16']),
    P("Résultat : `161`. Larkhré a collé le texte « 16 » et le nombre 1 ! Pour convertir un texte en vrai "
      "nombre, on l'enveloppe dans `nombre(...)` :"),
    CODE('laz age = nombre(demand("Ton âge ? "))\nvox("L\'année prochaine tu auras", age + 1, "ans")',
         ecran=True, entrees=['16']),
    P("Lis la ligne de l'intérieur vers l'extérieur : `demand(...)` récupère le texte « 16 », puis "
      "`nombre(...)` le transforme en 16, et le tout atterrit dans la boîte `age`. Emboîter des "
      "commandes ainsi, c'est du code de professionnel, et tu viens de le faire au chapitre 3."),
    EX('À toi de jouer — Exercices 3', [
        ("3.1", "Demande le plat préféré de l'utilisateur et réponds « Excellent choix, le {plat} ! »."),
        ("3.2", "Demande deux nombres et affiche leur somme, leur produit et leur moyenne."),
        ("3.3", "Demande l'année de naissance et calcule l'âge approximatif en 2026."),
    ]),
])

chapitre('Le cerveau du programme', 4, 'Décider : kan et sinon', [
    P("Le vrai pouvoir commence ici. Un programme intelligent ne fait pas toujours la même chose : il "
      "regarde la situation et choisit. En Larkhré, on décide avec `kan` (« quand ») :"),
    CODE('laz age = nombre(demand("Ton âge ? "))\nkan age >= 18 {\n    vox("Tu es majeur.")\n} sinon {\n'
         '    vox("Encore", 18 - age, "ans de patience !")\n}', ecran=True, entrees=['15']),
    P("Lis-le comme du français : « quand l'âge est supérieur ou égal à 18, fais ceci, sinon fais cela ». "
      "Les accolades `{ }` délimitent le bloc d'ordres concerné : tout ce qui est entre elles ne "
      "s'exécute que si la condition est vraie."),
    H2('Les comparaisons'),
    P("`==` égal (deux signes : un seul, c'est « mets dedans »), `!=` différent, `<` plus petit, "
      "`>` plus grand, `<=` et `>=` avec égalité. Chaque comparaison donne un booléen, `vrai` ou `faux`, "
      "les valeurs du chapitre 2. `kan` exécute son bloc quand la condition vaut `vrai`."),
    H2('Plusieurs cas : sinon kan'),
    CODE('laz note = nombre(demand("Ta note sur 20 ? "))\nkan note >= 16 {\n    vox("Excellent !")\n'
         '} sinon kan note >= 10 {\n    vox("C\'est réussi.")\n} sinon kan note >= 8 {\n'
         '    vox("Presque... courage !")\n} sinon {\n    vox("On révise ensemble ?")\n}', entrees=['12']),
    P("Larkhré teste les conditions dans l'ordre et exécute le premier bloc qui correspond, un seul."),
    H2('Combiner : et, ou, non'),
    CODE('kan age >= 12 et age <= 17 {\n    vox("Tarif ado !")\n}\n'
         'kan jour == "samedi" ou jour == "dimanche" {\n    vox("C\'est le week-end !")\n}',
         avant='laz age = 14\nlaz jour = "samedi"'),
    ASTUCE("Le piège classique : écrire `kan age = 18` au lieu de `kan age == 18`. Larkhré refuse le "
           "programme et t'indique la ligne : il attendait l'accolade `{`, et il a trouvé un `=`. "
           "Quand tu vois ce message sur une ligne `kan`, pense tout de suite au double `==`."),
    EX('À toi de jouer — Exercices 4', [
        ("4.1", "Demande un nombre et dis s'il est positif, négatif ou nul."),
        ("4.2", "Demande un nombre et dis s'il est pair ou impair. Indice : un nombre pair a un reste de "
                "zéro quand on le divise par 2, soit `nombre % 2 == 0`."),
        ("4.3", "Le videur de concert : entrée interdite avant 16 ans, tarif réduit de 16 à 25 ans, "
                "plein tarif après. Demande l'âge et affiche le bon message."),
    ]),
])

chapitre('Le cerveau du programme', 5, 'Répéter : les boucles', [
    P("Les machines ne se fatiguent jamais : c'est leur superpouvoir, et les boucles sont la façon de "
      "l'exploiter. Première boucle, `pou ... dan` (« pour ... dans ») :"),
    CODE('pou i dan 1..5 {\n    vox("Tour numéro {i}")\n}', ecran=True),
    P("`1..5` est un intervalle : tous les nombres de 1 à 5. La variable `i` prend chaque valeur à tour "
      "de rôle, et le bloc s'exécute pour chacune. La table de multiplication devient un jeu d'enfant :"),
    CODE('laz n = nombre(demand("Quelle table ? "))\npou i dan 1..10 {\n    vox("{n} × {i} =", n * i)\n}',
         entrees=['7']),
    H2('Voir la boucle vivre : ralenti()'),
    P("Dans le playground, ajoute cette ligne en haut de ton programme :"),
    CODE('ralenti(0.5)'),
    P("Exécute… et regarde : la ligne en cours s'illumine dans l'éditeur, et un panneau montre tes "
      "variables changer en direct, tour après tour. C'est l'un des super-pouvoirs de Larkhré. Utilise "
      "`ralenti` chaque fois qu'une boucle t'embrouille : c'est comme regarder un match au ralenti."),
    H2('Tant que : tanke'),
    P("`pou` répète un nombre de fois connu d'avance. `tanke` (« tant que ») répète tant qu'une condition "
      "reste vraie, sans savoir combien de temps ça durera :"),
    CODE('laz energie = 100\ntanke energie > 0 {\n    vox("Je danse ! Énergie : {energie}")\n'
         '    energie -= 30\n}\nvox("Épuisé. Dodo.")', ecran=True),
    ASTUCE("Si ta condition ne devient jamais fausse, la boucle tourne pour toujours : la fameuse "
           "« boucle infinie ». Pas de panique : au bout de quelques secondes, Larkhré l'arrête proprement "
           "avec un message. Essaie `tanke vrai { vox(\"aide\") }` pour voir : casser les choses exprès, "
           "c'est apprendre."),
    P("Deux outils de contrôle pour finir : `kase` casse la boucle immédiatement, et `swiv` saute "
      "directement au tour suivant."),
    EX('À toi de jouer — Exercices 5', [
        ("5.1", "Affiche le compte à rebours de 10 à 1 puis « Décollage ! ». Indice : `10..1` compte à "
                "l'envers tout seul."),
        ("5.2", "Calcule la somme de tous les nombres de 1 à 100 (Gauss l'a fait de tête à 8 ans, toi tu "
                "as une boucle)."),
        ("5.3", "Affiche les nombres de 1 à 30, mais remplace les multiples de 3 par « Zap ! ». "
                "Indice : `%` et `swiv`, ou bien `kan` / `sinon`."),
    ]),
])

chapitre('Le cerveau du programme', 6, 'Projet : le nombre mystère', [
    P("Tu as maintenant tout ce qu'il faut pour créer un vrai jeu : variables, conditions, boucles, "
      "dialogue. La machine choisit un nombre secret entre 1 et 100, à toi de le deviner, elle te guide. "
      "Avant de lire le code, note la nouveauté : `hasard(1, 100)` donne un nombre au hasard entre 1 et 100."),
    CODE('vox("=== LE NOMBRE MYSTÈRE ===")\nvox("J\'ai choisi un nombre entre 1 et 100...")\n'
         'laz secret = hasard(1, 100)\nlaz trouve = faux\nlaz essais = 0\n\ntanke non trouve {\n'
         '    laz nb = nombre(demand("Ton essai : "))\n    essais += 1\n    kan nb == secret {\n'
         '        trouve = vrai\n        vox("BRAVO ! Trouvé en {essais} essais !")\n'
         '    } sinon kan nb < secret {\n        vox("C\'est plus grand !")\n    } sinon {\n'
         '        vox("C\'est plus petit !")\n    }\n}',
         entrees=[str(n) for n in range(1, 101)]),
    P("Tape-le, joue, et surtout relis-le ligne par ligne en te racontant l'histoire : la boucle tourne "
      "« tant que non trouvé » ; à chaque tour on demande, on compte l'essai, on compare. Ce squelette "
      "(boucle, condition, variable d'état) est celui de milliers de vrais programmes."),
    EX('Améliore ton jeu', [
        ("6.1", "Limite à 7 essais maximum : au-delà, « Perdu ! Le nombre était {secret} ». "
                "Indice : `tanke non trouve et essais < 7`."),
        ("6.2", "Ajoute un commentaire selon la performance finale : 3 essais ou moins, « Légende ! » ; "
                "moins de 6, « Très fort » ; sinon « Bien joué quand même »."),
        ("6.3", "Version couleur : `vox_couleur(\"C'est plus grand !\", \"vert\")`, et `\"rouge\"` pour "
                "plus petit."),
    ]),
])

chapitre("Organiser l'information", 7, 'Les listes', [
    P("Une variable range une valeur. Une liste en range autant que tu veux, dans l'ordre, entre crochets :"),
    CODE('laz courses = ["riz", "tomates", "poisson"]\nlaz notes = [12, 15, 9, 18]'),
    P("Chaque élément a une position… et voici le piège à connaître une fois pour toutes : on compte à "
      "partir de zéro."),
    CODE('vox(courses[0])    # riz : le PREMIER est en 0\nvox(courses[2])    # poisson\n'
         'vox(courses[-1])   # poisson : -1 = le dernier', ecran=True,
         avant='laz courses = ["riz", "tomates", "poisson"]'),
    P("La boîte à outils des listes :"),
    CODE('ajoute(courses, "mangues")      # ajouter à la fin\nretire(courses, 0)              # retirer la position 0\n'
         'courses[1] = "oignons"          # remplacer\nvox(taille(courses))            # combien ?\n'
         'vox(tri(notes))                 # version triée\nvox(contient(courses, "riz"))   # vrai ou faux',
         avant='laz courses = ["riz", "tomates", "poisson"]\nlaz notes = [12, 15, 9, 18]'),
    H2('Le duo magique : liste et boucle'),
    P("`pou ... dan` sait parcourir une liste directement, c'est là que tout s'assemble :"),
    CODE('laz notes = [12, 15, 9, 18]\nlaz total = 0\npou note dan notes {\n    total += note\n}\n'
         'vox("Moyenne :", total / taille(notes))', ecran=True),
    EX('À toi de jouer — Exercices 7', [
        ("7.1", "Crée la liste de tes 4 plats préférés et affiche « J'adore le {plat} ! » pour chacun."),
        ("7.2", "Dans `[14, 7, 19, 3, 16]`, trouve le plus grand nombre avec une boucle (sans `tri` !). "
                "Indice : une variable `record` qu'on met à jour avec `kan`."),
        ("7.3", "Compte combien de notes de `[12, 8, 15, 9, 18, 6]` sont au-dessus de 10."),
    ]),
])

chapitre("Organiser l'information", 8, 'Les fonctions, tes propres commandes', [
    P("Tu utilises `vox()`, `hasard()`, `taille()` depuis le début. Il est temps de créer les tiennes. "
      "Une fonction, c'est une recette : on lui donne un nom, des ingrédients, et on peut la resservir "
      "à l'infini. Mot-clé : `fonk`."),
    CODE('fonk saluer(prenom) {\n    vox("Bonjour {prenom}, bienvenue !")\n}\n\nsaluer("Awa")\n'
         'saluer("Moussa")\nsaluer("Fatou")', ecran=True),
    P("Trois lignes d'appel, zéro répétition de logique. C'est la règle d'or des programmeurs : si tu "
      "écris deux fois la même chose, fais-en une fonction."),
    H2('rend : la fonction qui répond'),
    P("Une fonction peut renvoyer un résultat avec `rend`. On récupère alors sa réponse comme n'importe "
      "quelle valeur :"),
    CODE('fonk carre(x) {\n    rend x * x\n}\n\nfonk moyenne(liste) {\n    laz total = 0\n'
         '    pou n dan liste {\n        total += n\n    }\n    rend total / taille(liste)\n}\n\n'
         'vox(carre(8))\nvox(moyenne([12, 15, 9, 18]))', ecran=True),
    P("Regarde `moyenne` : c'est ton exercice du chapitre 7, devenu un outil réutilisable pour toujours. "
      "Voilà comment les programmeurs construisent : brique par brique."),
    ASTUCE("Dès que `rend` s'exécute, la fonction s'arrête et renvoie sa réponse, comme quelqu'un qui "
           "quitte la pièce après avoir répondu à ta question."),
    EX('À toi de jouer — Exercices 8', [
        ("8.1", "Écris `fonk double(x)` qui rend le double, puis affiche le double de 21."),
        ("8.2", "Écris `fonk plus_grand(a, b)` qui rend le plus grand des deux."),
        ("8.3", "Écris `fonk note_finale(controle, examen)` : le contrôle compte pour 40 %, l'examen "
                "pour 60 %. Teste avec 12 et 15."),
    ]),
])

chapitre("Organiser l'information", 9, 'Les dictionnaires', [
    P("Une liste range par position. Un dictionnaire range par étiquette, comme un annuaire : tu "
      "cherches un nom, tu obtiens une info. On l'écrit avec des accolades et des paires `\"clé\": valeur` :"),
    CODE('laz joueur = {\n    "nom": "Awa",\n    "score": 1250,\n    "niveau": 3\n}\n\n'
         'vox(joueur["nom"])     # Awa\njoueur["score"] += 50    # modifier\n'
         'joueur["vies"] = 3        # ajouter une nouvelle clé'),
    P("Outils du dictionnaire : `taille(d)`, `cles(d)` (la liste des étiquettes), `valeurs(d)`, "
      "`contient(d, \"nom\")`, `retire(d, \"vies\")`. Et la boucle parcourt les clés :"),
    CODE('pou cle dan joueur {\n    vox("{cle} :", joueur[cle])\n}', ecran=True,
         avant='laz joueur = { "nom": "Awa", "score": 1250, "niveau": 3 }\njoueur["score"] += 50\njoueur["vies"] = 3'),
    P("Liste ou dictionnaire ? Pose-toi la question : « mes données sont-elles une file ordonnée (liste) "
      "ou une fiche d'informations (dictionnaire) ? » Un panier de courses : liste. La fiche d'un élève : "
      "dictionnaire. Et on peut les combiner : une liste de dictionnaires, c'est exactement ce "
      "qu'utilisent les vraies applications."),
    EX('À toi de jouer — Exercices 9', [
        ("9.1", "Crée ta propre fiche (nom, ville, âge, passion) et affiche-la joliment avec une boucle."),
        ("9.2", "Crée un dictionnaire `prix` (`{\"pain\": 250, \"lait\": 500, \"riz\": 400}`) et calcule "
                "le total de toutes les valeurs."),
        ("9.3", "Mini-traducteur : un dictionnaire français-anglais de 5 mots ; demande un mot à "
                "l'utilisateur et affiche sa traduction (avec `contient` pour gérer les mots inconnus !)."),
    ]),
])

chapitre("Organiser l'information", 10, 'Projet : le quiz à record', [
    P("Deuxième grand projet, avec une nouveauté de Larkhré : la variable `garde`, qui se souvient "
      "entre les exécutions. Ton quiz gardera le record : ferme le programme, reviens demain, il s'en souvient."),
    CODE('garde record = 0\n\nlaz questions = [\n    { "q": "Capitale du Mali ?", "r": "bamako" },\n'
         '    { "q": "7 × 8 ?", "r": "56" },\n    { "q": "Créateur de Larkhré ?", "r": "ladji" }\n]\n\n'
         'laz score = 0\npou question dan questions {\n'
         '    laz reponse = minus(demand(question["q"] + " "))\n    laz bonne = question["r"]\n    kan reponse == bonne {\n'
         '        vox_couleur("Correct !", "vert")\n        score += 1\n    } sinon {\n'
         '        vox_couleur("Raté ! C\'était " + bonne, "rouge")\n    }\n}\n\n'
         'vox("Score final : {score} /", taille(questions))\nkan score > record {\n    record = score\n'
         '    vox_couleur("NOUVEAU RECORD : {record} !", "or")\n} sinon {\n'
         '    vox("Le record reste à {record}.")\n}', ecran=True, entrees=['Bamako', '54', 'Ladji']),
    P("Tout y est : liste de dictionnaires, boucle, condition, fonctions intégrées (`minus` met en "
      "minuscules pour accepter « Bamako » comme « BAMAKO »), couleurs, et la mémoire persistante."),
    EX('Améliore ton quiz', [
        ("10.1", "Ajoute 5 questions à toi (culture, foot, musique…)."),
        ("10.2", "Ajoute un pourcentage de réussite : `score / taille(questions) * 100`."),
        ("10.3", "Compte aussi le nombre total de parties jouées avec une deuxième variable `garde`."),
    ]),
])

chapitre('Les super-pouvoirs', 11, 'Dessine avec ton code', [
    P("Larkhré sait dessiner, et coder des images est l'une des plus belles façons de comprendre les "
      "boucles. Dans le playground, une toile apparaît et se dessine sous tes yeux :"),
    CODE('# la zone de dessin : largeur, hauteur\ntoile(400, 300)\n# le soleil : x, y, rayon, couleur\n'
         'cercle_plein(330, 60, 35, "or")\n# le sol : x1, y1, x2, y2, couleur\ntrace_ligne(0, 250, 400, 250, "vert")\n'
         '# la maison : x, y, largeur, hauteur, couleur\nrect_plein(80, 170, 120, 80, "gris")\n'
         'trace_texte(150, 40, "Chez moi", "cyan")'),
    P("Le point (0, 0) est le coin en haut à gauche ; x va vers la droite, y descend. Couleurs : rouge, "
      "vert, jaune, bleu, violet, cyan, blanc, or, gris, rose, noir. Autres formes : `trace_rect` et "
      "`trace_cercle` (contours seuls), et `fond(couleur)` pour peindre l'arrière-plan."),
    H2("La boucle artiste"),
    P("Le vrai spectacle commence quand les boucles dessinent :"),
    CODE('toile(400, 200)\npou i dan 1..8 {\n    cercle_plein(i * 45, 100, i * 4, "cyan")\n}'),
    P("Huit cercles de plus en plus grands, en quatre lignes. Change les nombres, mets `i * 10`, essaie "
      "d'autres couleurs : c'est en bidouillant qu'on devient créatif. Et sur ton ordinateur, avec "
      "Larkhré installé, `sauve_dessin(\"mon_dessin.svg\")` exporte ton œuvre en vraie image."),
    EX('Projet : ta carte de vœux', [
        ("11.1", "Crée une carte (400 × 300) pour quelqu'un que tu aimes : un fond de couleur, au moins "
                 "3 formes, un ciel d'étoiles fait par une boucle, et un message avec `trace_texte`. "
                 "C'est ta création : il n'y a pas de mauvaise réponse en art."),
    ]),
])

chapitre('Les super-pouvoirs', 12, 'Les objets : klas', [
    P("Dernier grand concept, celui qui structure les applications du monde entier. Une `klas` est un "
      "moule : tu le définis une fois, puis tu fabriques autant d'objets que tu veux avec."),
    CODE('klas Heros {\n    fonk init(moi, nom) {\n        moi.nom = nom\n        moi.vie = 100\n    }\n\n'
         '    fonk attaque(moi, degats) {\n        moi.vie -= degats\n'
         '        vox("Aïe !", moi.nom, "- vie restante :", moi.vie)\n    }\n}\n\n'
         'laz awa = Heros("Awa")\nlaz issa = Heros("Issa")\nawa.attaque(30)\nissa.attaque(15)\n'
         'vox(awa.vie, "contre", issa.vie)', ecran=True),
    P("Décodage : `init` est la recette de fabrication (elle s'exécute à chaque `Heros(...)`) ; `moi` "
      "désigne l'objet en train d'agir. Quand `awa.attaque(30)` s'exécute, `moi`, c'est Awa, et seule "
      "sa vie baisse. Chaque objet a sa propre mémoire : c'est toute la puissance du concept."),
    ASTUCE("Pour afficher une propriété, passe-la à `vox` avec une virgule, comme `moi.nom` ci-dessus. "
           "Les accolades dans un texte, comme `{nom}`, marchent avec une variable simple, pas avec "
           "`moi.nom`."),
    P("Bonus : une `klas` peut hériter d'une autre avec `herite`. Elle reçoit toutes ses capacités et "
      "ajoute les siennes. Tu trouveras un exemple complet dans le guide du langage ; pour l'instant, "
      "savoir créer un moule et ses objets te place déjà au-dessus de la plupart des débutants."),
    EX('À toi de jouer — Exercices 12', [
        ("12.1", "Crée une `klas Compte` (banque) avec `init(moi, titulaire)` qui met `moi.solde = 0`, "
                 "une fonction `depose(moi, montant)` et une fonction `affiche(moi)`."),
        ("12.2", "Fabrique deux comptes, dépose des montants différents, affiche les deux, et vérifie que "
                 "chaque compte garde bien son argent."),
    ]),
])

chapitre('Les super-pouvoirs', 13, 'Dompter les erreurs', [
    P("Vérité de programmeur : on passe plus de temps avec les erreurs qu'avec les succès, et c'est très "
      "bien. Chaque erreur est une leçon personnalisée. Larkhré est conçu pour être un bon prof "
      "d'erreurs : il te parle en français, et il te raconte même le film d'avant le plantage :"),
    CODE('laz total = 100\nlaz eleves = ["Awa", "Issa"]\nlaz nb_eleves = 0\nvox(total / nb_eleves)',
         ecran=True, attendu='erreur'),
    P("Lis le film : on voit tout de suite que `nb_eleves` valait 0 juste avant la division. "
      "L'enquête est résolue."),
    H2('Rattraper les erreurs : essaie et rattrape'),
    P("Un programme sérieux ne s'écroule pas quand l'utilisateur tape n'importe quoi : il rattrape."),
    CODE('essaie {\n    laz age = nombre(demand("Ton âge ? "))\n    vox("Dans 10 ans, tu auras", age + 10, "ans")\n'
         '} rattrape probleme {\n    vox("Ce n\'était pas un nombre ! ({probleme})")\n}\n'
         'vox("Le programme continue tranquillement.")', ecran=True, entrees=['seize']),
    P("Si tout va bien, le bloc `essaie` s'exécute normalement. Si une erreur survient, au lieu de "
      "planter, le programme saute dans le bloc `rattrape`, avec le message d'erreur rangé dans la "
      "variable. Et tu peux lever tes propres erreurs avec `echoue(\"message\")` quand une règle de ton "
      "programme est violée."),
    ASTUCE("Ton rituel de débogage : 1) lis le message, il est en français ; 2) regarde le film ; "
           "3) ajoute `ralenti(0.5)` et regarde les variables vivre. Avec ces trois outils, aucun bug "
           "ne te résistera longtemps."),
    EX('À toi de jouer — Exercices 13', [
        ("13.1", "Reprends le programme de l'âge du chapitre 3 : si l'utilisateur tape autre chose qu'un "
                 "nombre, rattrape l'erreur et affiche un message gentil au lieu de planter."),
        ("13.2", "Écris `fonk retirer(solde, montant)` qui fait `echoue(\"solde insuffisant !\")` si le "
                 "montant dépasse le solde, puis appelle-la dans un `essaie` / `rattrape`."),
    ]),
])

chapitre('Les super-pouvoirs', 14, 'Et maintenant ? Ton avenir de programmeur', [
    P("Fais le compte de ce que tu sais : variables, dialogue, conditions, boucles, listes, fonctions, "
      "dictionnaires, objets, gestion d'erreurs, dessin, et deux projets complets. Ce sont exactement "
      "les fondations de tous les langages. Python, JavaScript, Java : mêmes concepts, autres mots-clés."),
    H2('Tes prochaines étapes'),
    LISTE([
        "**Crée sans permission.** Un convertisseur de monnaie, un journal intime avec `ecris_fichier`, "
        "un pierre-feuille-ciseaux, un gestionnaire de devoirs… Le meilleur exercice est celui que tu inventes.",
        "**Passe à Python.** Sur ton ordinateur : `pip install larkhre`, puis "
        "`larkhre --traduire ton_programme.laz` transforme ton code en vrai Python, souvent environ "
        "10 fois plus rapide. Ouvre le fichier créé : tu liras du Python en connaissant déjà "
        "l'histoire qu'il raconte. C'est ta passerelle.",
        "**Change de langue.** `#langue: anglais` en tête de fichier, et tes mots-clés deviennent "
        "`let`, `func`, `when`… Il existe aussi `#langue: bambara` et `#langue: wolof`.",
        "**Montre ton code.** Le playground se partage par simple lien. Apprends à quelqu'un ce que tu "
        "viens d'apprendre : enseigner, c'est apprendre deux fois.",
    ]),
    P("Un dernier mot. Ce livre a été écrit avec un langage créé par une seule personne, partie de zéro, "
      "comme toi aujourd'hui. La programmation n'appartient à personne : ni à un pays, ni à une langue, "
      "ni à un diplôme. Elle appartient à ceux qui tapent la ligne suivante."),
    CODE('garde reves_realises = 0\nreves_realises += 1\nvox("À toi de jouer.")'),
])

# ---------------------------------------------------------------------------
SOLUTIONS = [
    P("Compare avec tes réponses, et souviens-toi qu'en programmation il existe toujours plusieurs bonnes "
      "solutions. Si la tienne marche et se lit bien, elle est bonne. Voici une sélection des exercices clés."),
    H2('1.3 — Guillemets ou pas'),
    P("`vox(\"2 + 3\")` affiche `2 + 3` (un texte, recopié tel quel) ; `vox(2 + 3)` affiche `5` (un calcul, exécuté)."),
    H2('2.3 — La copie'),
    P("Affiche `10 5` : à la ligne 2, `b` reçoit une copie de la valeur 5 ; changer `a` ensuite ne touche pas `b`."),
    H2('4.2 — Pair ou impair'),
    CODE('laz n = nombre(demand("Un nombre ? "))\nkan n % 2 == 0 {\n    vox("{n} est pair")\n} sinon {\n'
         '    vox("{n} est impair")\n}', entrees=['7']),
    H2('5.2 — La somme de Gauss'),
    CODE('laz somme = 0\npou i dan 1..100 {\n    somme += i\n}\nvox(somme)', ecran=True),
    H2('7.2 — Le plus grand'),
    CODE('laz nombres = [14, 7, 19, 3, 16]\nlaz record = nombres[0]\npou n dan nombres {\n'
         '    kan n > record {\n        record = n\n    }\n}\nvox("Le plus grand :", record)', ecran=True),
    H2('8.2 — plus_grand'),
    CODE('fonk plus_grand(a, b) {\n    kan a > b {\n        rend a\n    }\n    rend b\n}'),
    H2('9.3 — Mini-traducteur'),
    CODE('laz dico = {\n    "bonjour": "hello",\n    "merci": "thank you",\n    "eau": "water"\n}\n'
         'laz mot = minus(demand("Un mot en français ? "))\nkan contient(dico, mot) {\n'
         '    vox("En anglais : " + dico[mot])\n} sinon {\n    vox("Je ne connais pas encore ce mot !")\n}',
         entrees=['Merci']),
    H2('12.1 et 12.2 — La klas Compte'),
    CODE('klas Compte {\n    fonk init(moi, titulaire) {\n        moi.titulaire = titulaire\n        moi.solde = 0\n    }\n\n'
         '    fonk depose(moi, montant) {\n        moi.solde += montant\n    }\n\n'
         '    fonk affiche(moi) {\n        vox(moi.titulaire, ":", moi.solde, "F")\n    }\n}\n\n'
         'laz a = Compte("Awa")\nlaz m = Compte("Moussa")\na.depose(500)\nm.depose(1200)\na.affiche()\nm.affiche()',
         ecran=True),
    H2("13.1 — L'âge, sans planter"),
    CODE('essaie {\n    laz age = nombre(demand("Ton âge ? "))\n    vox("L\'année prochaine tu auras", age + 1, "ans")\n'
         '} rattrape erreur {\n    vox("Oups, tape ton âge en chiffres, par exemple 16.")\n}',
         ecran=True, entrees=['seize']),
]
