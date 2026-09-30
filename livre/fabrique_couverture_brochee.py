# -*- coding: utf-8 -*-
"""Couverture complète du livre broché pour Amazon KDP : quatrième + dos + première,
avec 0,125 pouce de fond perdu. Format A5 (5,83 × 8,27 pouces).

    python3 livre/fabrique_couverture_brochee.py [nombre_de_pages] [blanc|creme]
"""
import io, os, sys
from PIL import Image
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.colors import HexColor, white
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph, Frame
from reportlab.lib.styles import ParagraphStyle
import reportlab.rl_config as rl

ICI = os.path.dirname(os.path.abspath(__file__))
PAGES = int(sys.argv[1]) if len(sys.argv) > 1 else 40
PAPIER = sys.argv[2] if len(sys.argv) > 2 else 'blanc'
PHOTO = sys.argv[3] if len(sys.argv) > 3 else os.path.join(ICI, 'couverture.jpg')
SORTIE = os.path.join(ICI, 'Apprends_a_coder_avec_Larkhre_1.2_couverture_brochee.pdf')

F = '/usr/share/fonts/truetype/crosextra/'
for nom, fichier in [('Texte', 'Caladea-Regular'), ('Texte-Gras', 'Caladea-Bold'), ('Texte-Italique', 'Caladea-Italic')]:
    pdfmetrics.registerFont(TTFont(nom, F + fichier + '.ttf'))
pdfmetrics.registerFont(TTFont('Code', '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'))
rl.canvas_basefontname = 'Texte'

POUCE = 72.0
TW, TH = 5.83, 8.27                      # format A5 chez KDP
FP = 0.125                               # fond perdu
DOS = PAGES * (0.002252 if PAPIER == 'blanc' else 0.0025)
LARGEUR = (FP + TW + DOS + TW + FP) * POUCE
HAUTEUR = (FP + TH + FP) * POUCE
X_DOS = (FP + TW) * POUCE
X_PREM = (FP + TW + DOS) * POUCE
TERRE, CRAIE, OCRE = HexColor('#2b2119'), HexColor('#eeede6'), HexColor('#d9a15a')

c = Canvas(SORTIE, pagesize=(LARGEUR, HAUTEUR), initialFontName='Texte')
c.setTitle('Couverture — Apprends à coder de zéro avec Larkhré')

# ---------- quatrième et dos : la terre
c.setFillColor(TERRE)
c.rect(0, 0, X_PREM + 1, HAUTEUR, stroke=0, fill=1)

# ---------- première : la photo du baobab, à 300 points par pouce
larg_prem = LARGEUR - X_PREM
photo = Image.open(PHOTO).convert('RGB')
cible = larg_prem / HAUTEUR
if photo.width / photo.height > cible:
    nw = int(photo.height * cible); x0 = (photo.width - nw) // 2
    photo = photo.crop((x0, 0, x0 + nw, photo.height))
else:
    nh = int(photo.width / cible); y0 = (photo.height - nh) // 2
    photo = photo.crop((0, y0, photo.width, y0 + nh))
px_l = int(larg_prem / POUCE * 300)
photo = photo.resize((px_l, int(px_l / cible)), Image.LANCZOS)
# voile de ciel fondu dans la photo elle-même : un dégradé continu, sans bandes
from PIL import ImageDraw
voile = Image.new('RGBA', photo.size, (0, 0, 0, 0))
dv = ImageDraw.Draw(voile)
h_voile = int(photo.height * 0.49)
for i in range(h_voile):
    a = int(246 * min(1, 1.25 * (1 - i / h_voile)) ** 1.1)
    dv.line([(0, i), (photo.width, i)], fill=(154, 174, 214, a))
photo = Image.alpha_composite(photo.convert('RGBA'), voile).convert('RGB')
tampon = io.BytesIO(); photo.save(tampon, 'JPEG', quality=92); tampon.seek(0)
c.drawImage(ImageReader(tampon), X_PREM, 0, larg_prem, HAUTEUR)

c.setFillAlpha(0.9); c.setFillColor(TERRE)
c.rect(X_PREM, 0, larg_prem, 1.75 * POUCE, stroke=0, fill=1)
c.setFillAlpha(1)

# textes de la première (zone sûre : 0,25 pouce des bords coupés)
g = X_PREM + 0.45 * POUCE
c.setFillColor(TERRE)
c.setFont('Texte-Gras', 54); c.drawString(g - 2, HAUTEUR - 1.35 * POUCE, 'Larkhré')
c.setFont('Texte-Italique', 13.5); c.drawString(g, HAUTEUR - 1.72 * POUCE, 'Mossi sef raanné : la langue de la machine')
c.setFont('Texte-Gras', 20); c.drawString(g, HAUTEUR - 2.3 * POUCE, 'Apprends à coder de zéro')
c.setFillColor(CRAIE)
c.setFont('Texte', 11.5)
c.drawString(g, 1.28 * POUCE, 'La méthode douce pour écrire tes premiers programmes,')
c.drawString(g, 1.08 * POUCE, 'avec le langage qui parle français et explique tes erreurs.')
c.setFont('Texte-Gras', 13); c.drawString(g, 0.6 * POUCE, 'Ladji Doucaré')
c.setFont('Texte-Italique', 10); c.drawRightString(LARGEUR - 0.45 * POUCE, 0.6 * POUCE, 'Édition 1.2')

# ---------- quatrième de couverture
st = ParagraphStyle('q', fontName='Texte', fontSize=11, leading=15.5, textColor=CRAIE, spaceAfter=7)
st_t = ParagraphStyle('qt', parent=st, fontName='Texte-Gras', fontSize=18.5, leading=23, spaceAfter=10)
st_l = ParagraphStyle('ql', parent=st, leftIndent=12, firstLineIndent=-10, spaceAfter=3.5)
st_s = ParagraphStyle('qs', parent=st, fontName='Texte-Gras')
st_u = ParagraphStyle('qu', parent=st, fontName='Code', fontSize=8.8, textColor=OCRE)
contenu = [
    Paragraph('Et si ton premier langage parlait ta\u00a0langue\u00a0?', st_t),
    Paragraph("En 14 chapitres et 3 projets complets, ce livre t'emmène de zéro jusqu'aux objets, au dessin par "
              "le code et à la gestion d'erreurs, avec Larkhré, un langage conçu pour les débutants francophones : "
              "erreurs expliquées en français, exécution au ralenti visible, variables qui se souviennent.", st),
]
for it in ["Rien à installer : tout se passe dans ton navigateur, même sur téléphone",
           "Des exercices corrigés à chaque chapitre",
           "Un jeu, un quiz à record et une œuvre d'art à créer toi-même",
           "Tous les exemples vérifiés avec le vrai moteur du langage"]:
    contenu.append(Paragraph('•&nbsp;&nbsp;' + it, st_l))
contenu += [Paragraph('&nbsp;', st),
            Paragraph('<i>Mossi sef raanné</i> : « la langue de la machine », en soninké.', st),
            Paragraph('Ladji Doucaré, créateur du langage Larkhré', st_s),
            Paragraph('larkhre.github.io · pip install larkhre', st_u)]
# le code-barres est ajouté par Amazon en bas à droite : on laisse cette zone vide
marge = FP * POUCE + 0.45 * POUCE
cadre = Frame(marge, 1.75 * POUCE, TW * POUCE - 0.9 * POUCE, HAUTEUR - 1.75 * POUCE - marge,
              leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, showBoundary=0)
cadre.addFromList(contenu, c)

c.showPage()
c.save()
print(f'Couverture écrite : {SORTIE}')
print(f'  {PAGES} pages, papier {PAPIER} : dos {DOS:.4f} po · couverture {LARGEUR / POUCE:.4f} × {HAUTEUR / POUCE:.4f} po')
