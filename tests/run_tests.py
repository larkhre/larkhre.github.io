#!/usr/bin/env python3
"""Lance chaque programme de tests/programmes sur les DEUX moteurs
(l'interpréteur Python et le moteur JavaScript du playground) et compare
leur sortie à la sortie attendue (fichier .attendu).

    python3 tests/run_tests.py            # lancer les tests
    python3 tests/run_tests.py --generer  # (re)créer les .attendu manquants

Un fichier .in à côté d'un programme contient les réponses tapées au clavier.
Si la première ligne du programme est « # test: contient <texte> », on vérifie
seulement que chaque moteur affiche ce texte (utile quand le détail peut varier,
comme le nombre de tours avant l'arrêt d'une boucle infinie).
"""
import os, shutil, subprocess, sys, tempfile

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.dirname(ICI)
PROGRAMMES = os.path.join(ICI, 'programmes')
INTERPRETEUR = next(os.path.join(RACINE, n) for n in ('larkhre.py', 'larkhre.py')
                    if os.path.exists(os.path.join(RACINE, n)))
DELAI = 120


def normalise(texte):
    return texte.rstrip('\n') + '\n'


def lance_python(prog, entrees):
    with tempfile.TemporaryDirectory() as dossier:   # dossier neuf : « garde » repart de zéro
        copie = os.path.join(dossier, os.path.basename(prog))
        shutil.copy(prog, copie)
        try:
            r = subprocess.run([sys.executable, INTERPRETEUR, copie], input=entrees, cwd=dossier,
                               capture_output=True, text=True, timeout=DELAI, encoding='utf-8')
        except subprocess.TimeoutExpired:
            return f'DÉLAI DÉPASSÉ ({DELAI} s) : le programme ne s’est pas arrêté\n'
        return normalise(r.stdout)


def lance_js(prog, fichier_entrees):
    args = ['node', os.path.join(ICI, 'run_js.js'), prog]
    if os.path.exists(fichier_entrees):
        args.append(fichier_entrees)
    try:
        r = subprocess.run(args, capture_output=True, text=True, timeout=DELAI, encoding='utf-8')
    except subprocess.TimeoutExpired:
        return f'DÉLAI DÉPASSÉ ({DELAI} s) : le programme ne s’est pas arrêté\n'
    if r.returncode != 0:
        return 'ERREUR DU LANCEUR JS :\n' + r.stderr
    return normalise(r.stdout)


def main():
    generer = '--generer' in sys.argv
    noms = sorted(n for n in os.listdir(PROGRAMMES) if n.endswith('.laz'))
    echecs = 0
    for nom in noms:
        prog = os.path.join(PROGRAMMES, nom)
        base = prog[:-4]
        fichier_entrees = base + '.in'
        entrees = open(fichier_entrees, encoding='utf-8').read() if os.path.exists(fichier_entrees) else ''
        attendu_chemin = base + '.attendu'
        py = lance_python(prog, entrees)
        js = lance_js(prog, fichier_entrees)
        premiere = open(prog, encoding='utf-8').readline().strip()
        if premiere.startswith('# test: contient '):
            cherche = premiere[len('# test: contient '):]
            manque = [m for m, sortie in (('Python', py), ('JavaScript', js)) if cherche not in sortie]
            if manque:
                echecs += 1
                print(f'✘ {nom} : « {cherche} » absent de la sortie du moteur ' + ' et '.join(manque))
            else:
                print(f'✔ {nom}')
            continue
        if generer and not os.path.exists(attendu_chemin):
            if py != js:
                print(f'✘ {nom} : les deux moteurs ne sont pas d’accord, .attendu non créé')
                echecs += 1
                continue
            with open(attendu_chemin, 'w', encoding='utf-8') as f:
                f.write(py)
            print(f'+ {nom} : .attendu créé')
            continue
        attendu = normalise(open(attendu_chemin, encoding='utf-8').read()) if os.path.exists(attendu_chemin) else None
        problemes = []
        if attendu is None:
            problemes.append('pas de fichier .attendu (lance avec --generer)')
        else:
            if py != attendu:
                problemes.append('moteur Python différent de l’attendu')
            if js != attendu:
                problemes.append('moteur JavaScript différent de l’attendu')
        if problemes:
            echecs += 1
            print(f'✘ {nom} : ' + ' ; '.join(problemes))
            if attendu is not None:
                for moteur, sortie in (('Python', py), ('JS', js)):
                    if sortie != attendu:
                        print(f'  --- attendu ---\n{attendu}  --- {moteur} ---\n{sortie}')
        else:
            print(f'✔ {nom}')
    print(f'\n{len(noms) - echecs}/{len(noms)} programmes OK sur les deux moteurs.')
    sys.exit(1 if echecs else 0)


if __name__ == '__main__':
    main()
