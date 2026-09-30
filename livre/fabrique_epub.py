# -*- coding: utf-8 -*-
"""Fabrique l'EPUB du livre (pour Amazon Kindle et les liseuses), à partir de contenu.py.
Comme pour le PDF, chaque exemple est d'abord exécuté par le vrai moteur Larkhré.

    python3 livre/fabrique_epub.py
"""
import builtins, contextlib, datetime, importlib.util, io, os, re, sys, uuid, zipfile
from html import escape

from PIL import Image, ImageDraw, ImageFont

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
from contenu import LIVRE, SOLUTIONS, PLAYGROUND

MOTEUR = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ICI, '..', 'larkhre.py')
SORTIE = sys.argv[2] if len(sys.argv) > 2 else os.path.join(ICI, 'Apprends_a_coder_avec_Larkhre_1.2.epub')
COUV_KINDLE = os.path.join(ICI, 'couverture_kindle.jpg')

# ---------------------------------------------------------------- le moteur
spec = importlib.util.spec_from_file_location('larkhre', MOTEUR)
lk = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lk)
ANSI = re.compile(r'\x1b\[[0-9;]*m')


def execute(source, entrees):
    reponses = list(entrees)
    tampon = io.StringIO()
    vrai_input = builtins.input

    def faux_input(invite=''):
        rep = reponses.pop(0) if reponses else ''
        print(invite + rep)
        return rep
    builtins.input = faux_input
    erreur = False
    try:
        with contextlib.redirect_stdout(tampon):
            interp = lk.Interpreter()
            try:
                interp.run(source)
            except lk.LazError as e:
                erreur = True
                print(e)
                if interp.histoire:
                    print("\n— Le film juste avant l'erreur :")
                    for (l, n, v) in interp.histoire:
                        print(f"   ligne {l} : {n} = {v}")
    finally:
        builtins.input = vrai_input
    return ANSI.sub('', tampon.getvalue()).rstrip('\n'), erreur


blocs = [b for ch in LIVRE for b in ch['blocs'] if b[0] == 'code'] + [b for b in SOLUTIONS if b[0] == 'code']
problemes = 0
for _, d in blocs:
    avant = (d['avant'] + '\n') if d['avant'] else ''
    d['sortie'], erreur = execute(avant + d['code'], d['entrees'])
    if erreur != (d['attendu'] == 'erreur'):
        print('✘ comportement inattendu :', d['code'].split('\n')[0]); problemes += 1
print(f'{len(blocs)} exemples exécutés, {problemes} problème(s).')
if problemes:
    sys.exit(1)

# ---------------------------------------------------------------- la couverture Kindle (1600 × 2560)
F = '/usr/share/fonts/truetype/crosextra/'
W, H = 1600, 2560
photo = Image.open(os.path.join(ICI, 'couverture.jpg')).convert('RGB')
ech = max(W / photo.width, H / photo.height)
photo = photo.resize((int(photo.width * ech), int(photo.height * ech)), Image.LANCZOS)
x0, y0 = (photo.width - W) // 2, (photo.height - H) // 2
couv = photo.crop((x0, y0, x0 + W, y0 + H)).convert('RGBA')
voile = Image.new('RGBA', (W, H), (0, 0, 0, 0))
dv = ImageDraw.Draw(voile)
for i in range(1250):                                  # ciel adouci en haut, pour le titre
    a = int(246 * min(1, 1.25 * (1 - i / 1250)) ** 1.1)
    dv.line([(0, i), (W, i)], fill=(154, 174, 214, a))
dv.rectangle([0, H - 620, W, H], fill=(43, 33, 25, 228))  # bandeau terre en bas
couv = Image.alpha_composite(couv, voile).convert('RGB')
d = ImageDraw.Draw(couv)
TERRE, CRAIE = (43, 33, 25), (238, 237, 230)
d.text((150, 230), 'Larkhré', font=ImageFont.truetype(F + 'Caladea-Bold.ttf', 250), fill=TERRE)
d.text((158, 545), 'Mossi sef raanné : la langue de la machine', font=ImageFont.truetype(F + 'Caladea-Italic.ttf', 64), fill=TERRE)
d.text((155, 690), 'Apprends à coder de zéro', font=ImageFont.truetype(F + 'Caladea-Bold.ttf', 112), fill=TERRE)
d.text((155, H - 520), 'La méthode douce pour écrire tes premiers', font=ImageFont.truetype(F + 'Caladea-Regular.ttf', 60), fill=CRAIE)
d.text((155, H - 440), 'programmes, avec le langage qui parle', font=ImageFont.truetype(F + 'Caladea-Regular.ttf', 60), fill=CRAIE)
d.text((155, H - 360), 'français et explique tes erreurs.', font=ImageFont.truetype(F + 'Caladea-Regular.ttf', 60), fill=CRAIE)
d.text((155, H - 210), 'Ladji Doucaré', font=ImageFont.truetype(F + 'Caladea-Bold.ttf', 78), fill=CRAIE)
d.text((W - 155, H - 196), 'Édition 1.2', font=ImageFont.truetype(F + 'Caladea-Italic.ttf', 56), fill=CRAIE, anchor='ra')
couv.save(COUV_KINDLE, quality=90)
petite = io.BytesIO()
couv.resize((800, 1280), Image.LANCZOS).save(petite, 'JPEG', quality=86)

# ---------------------------------------------------------------- le texte
def marque(texte):
    morceaux = re.split(r'(`[^`]+`)', texte)
    sortie = []
    for m in morceaux:
        if m.startswith('`') and m.endswith('`') and len(m) > 1:
            sortie.append('<code>' + escape(m[1:-1], quote=False) + '</code>')
        else:
            t = escape(m, quote=False)
            t = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', t)
            t = re.sub(r'\*(.+?)\*', r'<em>\1</em>', t)
            sortie.append(t)
    return ''.join(sortie)


def rend(blocs):
    h = []
    for b in blocs:
        k = b[0]
        if k == 'p':
            h.append('<p>' + marque(b[1]) + '</p>')
        elif k == 'h2':
            h.append('<h2>' + marque(b[1]) + '</h2>')
        elif k == 'adresse':
            h.append('<p class="adresse">' + escape(b[1]) + '</p>')
        elif k == 'astuce':
            h.append('<div class="astuce"><p class="titre-encadre">Astuce</p><p>' + marque(b[1]) + '</p></div>')
        elif k == 'liste':
            h.append('<ul>' + ''.join('<li>' + marque(i) + '</li>' for i in b[1]) + '</ul>')
        elif k == 'ex':
            h.append('<div class="exercices"><p class="titre-encadre">' + marque(b[1]) + '</p>'
                     + ''.join(f'<p class="ex"><strong>{n}</strong> {marque(t)}</p>' for n, t in b[2]) + '</div>')
        elif k == 'code':
            dd = b[1]
            h.append('<pre class="code">' + escape(dd['code'], quote=False) + '</pre>')
            if dd['ecran']:
                h.append('<p class="etiquette-ecran">À l\'écran :</p><pre class="ecran">'
                         + escape(dd['sortie'], quote=False) + '</pre>')
    return '\n'.join(h)


def page(titre, corps):
    return ('<?xml version="1.0" encoding="utf-8"?>\n<!DOCTYPE html>\n'
            '<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" lang="fr" xml:lang="fr">\n'
            f'<head><meta charset="utf-8"/><title>{escape(titre)}</title>'
            '<link rel="stylesheet" type="text/css" href="style.css"/></head>\n'
            f'<body>\n{corps}\n</body>\n</html>\n')


CSS = """
body { font-family: serif; line-height: 1.5; margin: 0 4%; }
h1 { font-size: 1.6em; margin: 0.4em 0 0.6em; line-height: 1.2; }
h2 { font-size: 1.2em; margin: 1.2em 0 0.4em; }
p { margin: 0 0 0.7em; text-indent: 0; }
.etiquette { font-style: italic; color: #b0702a; margin: 1.5em 0 0; }
code { font-family: monospace; font-size: 0.92em; }
pre { font-family: monospace; font-size: 0.85em; line-height: 1.35; white-space: pre-wrap;
      margin: 0.4em 0 0.8em; padding: 0.6em 0.8em; }
pre.code { background: #f4ede1; border-left: 3px solid #b0702a; }
pre.ecran { background: #243029; color: #eeede6; }
p.etiquette-ecran { font-style: italic; font-size: 0.85em; margin: 0; color: #6b5f55; }
.astuce { background: #eef0e2; padding: 0.5em 0.8em; margin: 0.8em 0; }
.exercices { border-left: 3px solid #b0702a; padding: 0.3em 0.8em; margin: 1em 0; }
.titre-encadre { font-weight: bold; color: #b0702a; margin-bottom: 0.3em; }
p.ex { margin-bottom: 0.4em; }
p.adresse { font-family: monospace; font-weight: bold; text-align: center; color: #b0702a; }
.titre-livre { text-align: center; margin-top: 3em; }
.titre-livre h1 { font-size: 2.4em; margin-bottom: 0.2em; }
.centre { text-align: center; }
nav ol { list-style: none; padding-left: 0; }
nav li { margin: 0.3em 0; }
"""

fichiers = []   # (id, nom, titre, xhtml)
fichiers.append(('titre', 'titre.xhtml', 'Apprends à coder de zéro avec Larkhré', page('Titre', f"""
<div class="titre-livre">
<h1>Larkhré</h1>
<p><em>Mossi sef raanné</em> : la langue de la machine</p>
<h2>Apprends à coder de zéro</h2>
<p>La méthode douce pour écrire tes premiers programmes, avec le langage qui parle français et explique tes erreurs.</p>
<p><strong>Ladji Doucaré</strong></p>
<p>Édition 1.2 — septembre 2026</p>
</div>
<p class="centre">Anciennement <em>Apprends à coder de zéro avec LAZARUS</em> (édition 1, août 2026). Le langage a changé de nom ; les programmes, eux, n'ont pas changé.</p>
<p class="centre"><strong>Tous les exemples de ce livre sont exécutés automatiquement</strong> par le moteur du langage au moment de fabriquer ce livre, et les résultats « À l'écran » sont ceux que le moteur affiche réellement.</p>
<p class="centre">Playground gratuit : <code>{PLAYGROUND}</code><br/>Sur ordinateur : <code>pip install larkhre</code></p>
<p class="centre"><em>© 2026 Ladji Doucaré. Le langage Larkhré est libre (licence MIT). Photo de couverture : Francesca Fabian, Unsplash.</em></p>
""")))
for i, ch in enumerate(LIVRE):
    lab = f"Chapitre {ch['numero']}" if ch['numero'] else 'Avant de commencer'
    corps = f'<p class="etiquette">{lab}</p>\n<h1>{escape(ch["titre"])}</h1>\n' + rend(ch['blocs'])
    titre_toc = (f"{ch['numero']}. " if ch['numero'] else '') + ch['titre']
    fichiers.append((f'ch{i}', f'chapitre{i:02d}.xhtml', titre_toc, page(ch['titre'], corps)))
fichiers.append(('sol', 'solutions.xhtml', 'Les solutions des exercices',
                 page('Solutions', '<p class="etiquette">Annexe</p>\n<h1>Les solutions des exercices</h1>\n' + rend(SOLUTIONS))))

nav_items = ''.join(f'<li><a href="{n}">{escape(t)}</a></li>' for (_, n, t, _) in fichiers[1:])
nav = page('Sommaire', f'<nav epub:type="toc" id="toc"><h1>Sommaire</h1><ol>{nav_items}</ol></nav>'
           '<nav epub:type="landmarks" hidden="hidden"><ol>'
           '<li><a epub:type="cover" href="couverture.xhtml">Couverture</a></li>'
           '<li><a epub:type="toc" href="nav.xhtml">Sommaire</a></li>'
           '<li><a epub:type="bodymatter" href="chapitre00.xhtml">Début</a></li></ol></nav>')
couv_xhtml = page('Couverture', '<div class="centre"><img src="couverture.jpg" alt="Couverture : Larkhré, apprends à coder de zéro" style="max-width:100%;height:auto"/></div>')

ident = 'urn:uuid:' + str(uuid.uuid5(uuid.NAMESPACE_URL, 'larkhre-livre-apprends-a-coder-1.2'))
maintenant = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
manifest = ['<item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>',
            '<item id="css" href="style.css" media-type="text/css"/>',
            '<item id="image-couverture" href="couverture.jpg" media-type="image/jpeg" properties="cover-image"/>',
            '<item id="couverture" href="couverture.xhtml" media-type="application/xhtml+xml"/>',
            '<item id="ncx" href="toc.ncx" media-type="application/x-dtbncx+xml"/>']
spine = ['<itemref idref="couverture" linear="yes"/>']
for (i, n, _, _) in fichiers:
    manifest.append(f'<item id="{i}" href="{n}" media-type="application/xhtml+xml"/>')
spine.insert(1, '<itemref idref="titre"/>')
spine.append('<itemref idref="nav"/>')
for (i, _, _, _) in fichiers[1:]:
    spine.append(f'<itemref idref="{i}"/>')
opf = f"""<?xml version="1.0" encoding="utf-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="uid" xml:lang="fr">
<metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
<dc:identifier id="uid">{ident}</dc:identifier>
<dc:title>Apprends à coder de zéro avec Larkhré</dc:title>
<dc:creator>Ladji Doucaré</dc:creator>
<dc:language>fr</dc:language>
<dc:publisher>Ladji Doucaré</dc:publisher>
<dc:date>2026-09-26</dc:date>
<dc:rights>© 2026 Ladji Doucaré</dc:rights>
<meta property="dcterms:modified">{maintenant}</meta>
<meta name="cover" content="image-couverture"/>
</metadata>
<manifest>
{chr(10).join(manifest)}
</manifest>
<spine toc="ncx">
{chr(10).join(spine)}
</spine>
</package>
"""
ncx_points = ''.join(f'<navPoint id="np{k}" playOrder="{k + 1}"><navLabel><text>{escape(t)}</text></navLabel><content src="{n}"/></navPoint>'
                     for k, (_, n, t, _) in enumerate(fichiers[1:]))
ncx = f"""<?xml version="1.0" encoding="utf-8"?>
<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1" xml:lang="fr">
<head><meta name="dtb:uid" content="{ident}"/></head>
<docTitle><text>Apprends à coder de zéro avec Larkhré</text></docTitle>
<navMap>{ncx_points}</navMap>
</ncx>
"""
container = """<?xml version="1.0" encoding="utf-8"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
<rootfiles><rootfile full-path="OEBPS/contenu.opf" media-type="application/oebps-package+xml"/></rootfiles>
</container>
"""

with zipfile.ZipFile(SORTIE, 'w') as z:
    z.writestr(zipfile.ZipInfo('mimetype'), 'application/epub+zip', compress_type=zipfile.ZIP_STORED)
    def ecrit(nom, data):
        z.writestr(nom, data, compress_type=zipfile.ZIP_DEFLATED)
    ecrit('META-INF/container.xml', container)
    ecrit('OEBPS/contenu.opf', opf)
    ecrit('OEBPS/toc.ncx', ncx)
    ecrit('OEBPS/nav.xhtml', nav)
    ecrit('OEBPS/style.css', CSS)
    ecrit('OEBPS/couverture.xhtml', couv_xhtml)
    ecrit('OEBPS/couverture.jpg', petite.getvalue())
    for (_, n, _, x) in fichiers:
        ecrit('OEBPS/' + n, x)
print('EPUB écrit :', SORTIE, '· couverture Kindle :', COUV_KINDLE)
