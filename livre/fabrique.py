# -*- coding: utf-8 -*-
"""Fabrique le PDF du livre. Chaque bloc de code est d'abord exécuté par le vrai
moteur Larkhré ; la fabrication s'arrête si un exemple ne se comporte pas comme prévu.

    python3 livre/fabrique.py                      (depuis la racine du dépôt)
    python3 livre/fabrique.py larkhre.py sortie.pdf
"""
import builtins, contextlib, importlib.util, io, os, re, sys
from xml.sax.saxutils import escape

from reportlab.lib.pagesizes import A5
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, white
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, Frame, PageTemplate, Paragraph, Spacer, Flowable,
                                KeepTogether, PageBreak, NextPageTemplate, Table, TableStyle, CondPageBreak)

from contenu import LIVRE, SOLUTIONS, PLAYGROUND

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
MOTEUR = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ICI, '..', 'larkhre.py')
SORTIE = sys.argv[2] if len(sys.argv) > 2 else os.path.join(ICI, 'Apprends_a_coder_avec_Larkhre_1.1.pdf')

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
        print(invite + rep)          # comme à l'écran : la question, puis ce qu'on a tapé
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


def verifie_tout():
    blocs = [b for ch in LIVRE for b in ch['blocs'] if b[0] == 'code'] + [b for b in SOLUTIONS if b[0] == 'code']
    problemes = 0
    for _, d in blocs:
        largeur = max(len(l) for l in d['code'].split('\n'))
        if largeur > 58:
            print('✘ ligne trop longue (', largeur, ') :', d['code'].split('\n')[0]); problemes += 1
        avant = (d['avant'] + '\n') if d['avant'] else ''
        sortie, erreur = execute(avant + d['code'], d['entrees'])
        if avant:
            sortie, _ = sortie, _     # le contexte n'affiche rien
        d['sortie'] = sortie
        if erreur != (d['attendu'] == 'erreur'):
            print('✘ comportement inattendu :', d['code'].split('\n')[0], '\n', sortie); problemes += 1
    print(f'{len(blocs)} exemples exécutés, {problemes} problème(s).')
    if problemes:
        sys.exit(1)


verifie_tout()

# ---------------------------------------------------------------- mise en page
F = '/usr/share/fonts/truetype/'
pdfmetrics.registerFont(TTFont('Texte', F + 'crosextra/Caladea-Regular.ttf'))
pdfmetrics.registerFont(TTFont('Texte-Gras', F + 'crosextra/Caladea-Bold.ttf'))
pdfmetrics.registerFont(TTFont('Texte-Italique', F + 'crosextra/Caladea-Italic.ttf'))
pdfmetrics.registerFont(TTFont('Texte-GrasItalique', F + 'crosextra/Caladea-BoldItalic.ttf'))
pdfmetrics.registerFont(TTFont('Code', F + 'dejavu/DejaVuSansMono.ttf'))
pdfmetrics.registerFont(TTFont('Code-Gras', F + 'dejavu/DejaVuSansMono-Bold.ttf'))
from reportlab.pdfbase.pdfmetrics import registerFontFamily
registerFontFamily('Texte', normal='Texte', bold='Texte-Gras', italic='Texte-Italique', boldItalic='Texte-GrasItalique')
registerFontFamily('Code', normal='Code', bold='Code-Gras', italic='Code', boldItalic='Code-Gras')

TERRE = HexColor('#2b2119'); OCRE = HexColor('#b0702a'); SABLE = HexColor('#f4ede1')
ARDOISE = HexColor('#243029'); CRAIE = HexColor('#eeede6'); KAKI = HexColor('#eef0e2'); GRIS = HexColor('#6b5f55')

LARG, HAUT = A5
MG, MD, MH, MB = 17 * mm, 15 * mm, 17 * mm, 18 * mm

corps = ParagraphStyle('corps', fontName='Texte', fontSize=10.6, leading=15, textColor=TERRE, spaceAfter=6)
h1 = ParagraphStyle('h1', fontName='Texte-Gras', fontSize=21, leading=25, textColor=TERRE, spaceAfter=10)
etiquette = ParagraphStyle('etiquette', fontName='Texte-Italique', fontSize=11, leading=14, textColor=OCRE, spaceAfter=2)
h2 = ParagraphStyle('h2', fontName='Texte-Gras', fontSize=13, leading=16, textColor=TERRE, spaceBefore=8, spaceAfter=4)
codest = ParagraphStyle('code', fontName='Code', fontSize=8.4, leading=11.2, textColor=TERRE)
ecranst = ParagraphStyle('ecran', fontName='Code', fontSize=8.4, leading=11.2, textColor=CRAIE)
petit = ParagraphStyle('petit', fontName='Texte-Italique', fontSize=9, leading=11, textColor=GRIS, spaceBefore=2, spaceAfter=1)
astuce_titre = ParagraphStyle('at', fontName='Texte-Gras', fontSize=10.2, leading=13, textColor=OCRE)
astuce_st = ParagraphStyle('as', parent=corps, fontSize=10, leading=14, spaceAfter=0)
ex_item = ParagraphStyle('ei', parent=corps, fontSize=10.2, leading=14, leftIndent=26, firstLineIndent=-26, spaceAfter=4)
liste_st = ParagraphStyle('li', parent=corps, leftIndent=12, firstLineIndent=-10)
adresse = ParagraphStyle('adr', fontName='Code-Gras', fontSize=10.5, leading=14, textColor=OCRE, alignment=TA_CENTER, spaceBefore=2, spaceAfter=8)
sommaire_partie = ParagraphStyle('sp', fontName='Texte-Italique', fontSize=10.5, leading=14, textColor=OCRE, spaceBefore=8, spaceAfter=2)


def marque(texte):
    """`code`, **gras**, *italique* → balises ReportLab (en protégeant le code)."""
    morceaux = re.split(r'(`[^`]+`)', texte)
    sortie = []
    for m in morceaux:
        if m.startswith('`') and m.endswith('`') and len(m) > 1:
            sortie.append('<font name="Code" size="8.9" color="#7a4a1c">' + escape(m[1:-1]) + '</font>')
        else:
            t = escape(m)
            t = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', t)
            t = re.sub(r'\*(.+?)\*', r'<i>\1</i>', t)
            sortie.append(t)
    return ''.join(sortie)


def bloc_texte(code, style):
    lignes = [escape(l).replace(' ', '&nbsp;') or '&nbsp;' for l in code.split('\n')]
    return Paragraph('<br/>'.join(lignes), style)


def encadre(contenu, fond, bord=None, pad=7):
    t = Table([[contenu]], colWidths=[LARG - MG - MD])
    st = [('BACKGROUND', (0, 0), (-1, -1), fond), ('LEFTPADDING', (0, 0), (-1, -1), pad + 3),
          ('RIGHTPADDING', (0, 0), (-1, -1), pad), ('TOPPADDING', (0, 0), (-1, -1), pad - 1),
          ('BOTTOMPADDING', (0, 0), (-1, -1), pad)]
    if bord:
        st.append(('LINEBEFORE', (0, 0), (0, -1), 2.2, bord))
    t.setStyle(TableStyle(st))
    return t


def rend_code(d):
    elements = [encadre(bloc_texte(d['code'], codest), SABLE, OCRE), Spacer(1, 3)]
    if d['ecran']:
        elements += [Paragraph("À l'écran :", petit), encadre(bloc_texte(d['sortie'], ecranst), ARDOISE), Spacer(1, 4)]
    elements.append(Spacer(1, 4))
    return KeepTogether(elements)


def rend(blocs):
    out = []
    for b in blocs:
        k = b[0]
        if k == 'p':
            out.append(Paragraph(marque(b[1]), corps))
        elif k == 'h2':
            out.append(CondPageBreak(40 * mm)); out.append(Paragraph(marque(b[1]), h2))
        elif k == 'code':
            out.append(rend_code(b[1]))
        elif k == 'astuce':
            out.append(Spacer(1, 3))
            out.append(KeepTogether([encadre([Paragraph('Astuce', astuce_titre), Paragraph(marque(b[1]), astuce_st)], KAKI)]))
            out.append(Spacer(1, 8))
        elif k == 'adresse':
            out.append(Paragraph(escape(b[1]), adresse))
        elif k == 'liste':
            for it in b[1]:
                out.append(Paragraph('•&nbsp;&nbsp;' + marque(it), liste_st))
        elif k == 'ex':
            items = [Paragraph(marque(b[1]), astuce_titre), Spacer(1, 4)]
            items += [Paragraph(f'<b>{n}</b>&nbsp;&nbsp;' + marque(t), ex_item) for n, t in b[2]]
            out.append(Spacer(1, 4))
            out.append(KeepTogether([encadre(items, white, OCRE)]))
            out.append(Spacer(1, 8))
    return out


class Repere(Flowable):
    """Invisible : note la page où commence un chapitre (pour le sommaire)."""
    def __init__(self, cle): super().__init__(); self.cle = cle
    def wrap(self, *a): return (0, 0)
    def draw(self): PAGES[self.cle] = self.canv.getPageNumber()


PAGES = {}
PAGES_AVANT = {}


def pied(canv, doc):
    n = canv.getPageNumber()
    canv.saveState()
    canv.setFont('Texte-Italique', 8.5); canv.setFillColor(GRIS)
    canv.drawString(MG, 10 * mm, 'Apprends à coder de zéro avec Larkhré')
    canv.drawRightString(LARG - MD, 10 * mm, str(n))
    canv.restoreState()


def couverture(canv, doc):
    canv.saveState()
    iw, ih = 1240, 1860
    echelle = max(LARG / iw, HAUT / ih)
    w, h = iw * echelle, ih * echelle
    canv.drawImage(os.path.join(ICI, 'couverture.jpg'), (LARG - w) / 2, (HAUT - h) / 2, w, h)
    for i in range(40):                       # voile de ciel en haut, pour le titre
        a = 0.93 * (1 - i / 40) ** 1.4
        canv.setFillColor(HexColor('#9aaed6')); canv.setFillAlpha(a)
        canv.rect(0, HAUT - (i + 1) * 3.2 * mm, LARG, 3.2 * mm, stroke=0, fill=1)
    canv.setFillAlpha(0.88); canv.setFillColor(TERRE)
    canv.rect(0, 0, LARG, 44 * mm, stroke=0, fill=1)
    canv.setFillAlpha(1)
    canv.setFillColor(TERRE)
    canv.setFont('Texte-Gras', 50); canv.drawString(MG - 1.5, HAUT - 38 * mm, 'Larkhré')
    canv.setFont('Texte-Italique', 12.5); canv.drawString(MG, HAUT - 47 * mm, 'Mosi larkhré : la langue de la machine')
    canv.setFont('Texte-Gras', 17); canv.drawString(MG, HAUT - 61 * mm, 'Apprends à coder de zéro')
    canv.setFillColor(CRAIE)
    canv.setFont('Texte', 10.5)
    canv.drawString(MG, 31 * mm, 'La méthode douce pour écrire tes premiers programmes,')
    canv.drawString(MG, 26 * mm, 'avec le langage qui parle français et explique tes erreurs.')
    canv.setFont('Texte-Gras', 12); canv.drawString(MG, 14 * mm, 'Ladji Doucaré')
    canv.setFont('Texte-Italique', 9); canv.drawRightString(LARG - MD, 14 * mm, 'Édition 1.1')
    canv.restoreState()


def quatrieme(canv, doc):
    canv.saveState()
    canv.setFillColor(TERRE); canv.rect(0, 0, LARG, HAUT, stroke=0, fill=1)
    canv.restoreState()


dos = ParagraphStyle('dos', parent=corps, textColor=CRAIE, fontSize=11, leading=16)
dos_titre = ParagraphStyle('dost', parent=h1, textColor=CRAIE, fontSize=19, leading=24)


def construit(fichier):
    doc = BaseDocTemplate(fichier, pagesize=A5, leftMargin=MG, rightMargin=MD, topMargin=MH, bottomMargin=MB,
                          title='Apprends à coder de zéro avec Larkhré', author='Ladji Doucaré',
                          subject='Édition 1.1 — 2026', creator='Larkhré')
    cadre = Frame(MG, MB, LARG - MG - MD, HAUT - MH - MB, id='c')
    doc.addPageTemplates([
        PageTemplate('couverture', [cadre], onPage=couverture),
        PageTemplate('page', [cadre], onPage=pied),
        PageTemplate('quatrieme', [cadre], onPage=quatrieme),
    ])
    h = [Spacer(1, 1), NextPageTemplate('page'), PageBreak()]

    # page de garde / édition
    h += [Spacer(1, 18 * mm), Paragraph('Apprends à coder de zéro avec Larkhré', h1),
          Paragraph('Édition 1.1 — septembre 2026', etiquette), Spacer(1, 8),
          Paragraph(marque("Anciennement *Apprends à coder de zéro avec LAZARUS* (édition 1, août 2026). "
                           "Le langage a changé de nom ; les programmes, eux, n'ont pas changé."), corps),
          Paragraph(marque("**Tous les exemples de ce livre sont exécutés automatiquement** par le moteur du "
                           "langage au moment de fabriquer ce livre, et les résultats « À l'écran » sont ceux "
                           "que le moteur affiche réellement."), corps),
          Paragraph(marque(f"Playground gratuit : `{PLAYGROUND}` · Sur ordinateur : `pip install larkhre`"), corps),
          Spacer(1, 10),
          Paragraph(marque("© 2026 Ladji Doucaré. Le langage Larkhré est libre (licence MIT). "
                           "Photo de couverture : Francesca Fabian, Unsplash."), petit),
          PageBreak()]

    # sommaire
    h += [Paragraph('Sommaire', h1), Spacer(1, 4)]
    partie = None
    lignes = []
    for i, ch in enumerate(LIVRE):
        if ch['partie'] != partie:
            partie = ch['partie']
            lignes.append(Paragraph(escape(partie), sommaire_partie))
        num = f"{ch['numero']}. " if ch['numero'] else ''
        page = PAGES_AVANT.get(f'ch{i}', '')
        t = Table([[Paragraph(escape(num + ch['titre']), corps), Paragraph(str(page), ParagraphStyle('pr', parent=corps, alignment=2))]],
                  colWidths=[LARG - MG - MD - 14 * mm, 14 * mm])
        t.setStyle(TableStyle([('LEFTPADDING', (0, 0), (-1, -1), 0), ('RIGHTPADDING', (0, 0), (-1, -1), 0),
                               ('TOPPADDING', (0, 0), (-1, -1), 0), ('BOTTOMPADDING', (0, 0), (-1, -1), -3)]))
        lignes.append(t)
    t = Table([[Paragraph('Les solutions des exercices', corps), Paragraph(str(PAGES_AVANT.get('sol', '')), ParagraphStyle('pr2', parent=corps, alignment=2))]],
              colWidths=[LARG - MG - MD - 14 * mm, 14 * mm])
    t.setStyle(TableStyle([('LEFTPADDING', (0, 0), (-1, -1), 0), ('RIGHTPADDING', (0, 0), (-1, -1), 0)]))
    h += lignes + [Spacer(1, 6), t, PageBreak()]

    for i, ch in enumerate(LIVRE):
        lab = f"Chapitre {ch['numero']}" if ch['numero'] else 'Avant de commencer'
        h += [Repere(f'ch{i}'), Paragraph(lab, etiquette), Paragraph(escape(ch['titre']), h1)]
        h += rend(ch['blocs'])
        h.append(PageBreak())
    h += [Repere('sol'), Paragraph('Annexe', etiquette), Paragraph('Les solutions des exercices', h1)]
    h += rend(SOLUTIONS)

    h += [NextPageTemplate('quatrieme'), PageBreak(), Spacer(1, 22 * mm),
          Paragraph('Et si ton premier langage parlait ta langue ?', dos_titre), Spacer(1, 6),
          Paragraph(marque("En 14 chapitres et 3 projets complets, ce livre t'emmène de zéro jusqu'aux objets, "
                           "au dessin par le code et à la gestion d'erreurs, avec Larkhré, un langage conçu pour "
                           "les débutants francophones : erreurs expliquées en français, exécution au ralenti "
                           "visible, variables qui se souviennent."), dos),
          Spacer(1, 4)]
    for it in ["Rien à installer : tout se passe dans ton navigateur, même sur téléphone",
               "Des exercices corrigés à chaque chapitre",
               "Un jeu, un quiz à record et une œuvre d'art à créer toi-même",
               "Une passerelle vers Python et vers l'anglais"]:
        h.append(Paragraph('•&nbsp;&nbsp;' + escape(it), ParagraphStyle('dl', parent=dos, leftIndent=12, firstLineIndent=-10, spaceAfter=3)))
    h += [Spacer(1, 12),
          Paragraph(marque("*Mosi larkhré* : « la langue de la machine », en soninké."), dos),
          Spacer(1, 14),
          Paragraph('Ladji Doucaré, créateur du langage Larkhré', ParagraphStyle('sig', parent=dos, fontName='Texte-Gras')),
          Paragraph(escape(PLAYGROUND) + ' · pip install larkhre', ParagraphStyle('url', parent=dos, fontName='Code', fontSize=8.8))]
    doc.build(h)


# deux passages : le premier mesure les pages des chapitres, le second écrit le sommaire
construit('/tmp/_brouillon.pdf')
PAGES_AVANT.update(PAGES)
PAGES.clear()
construit(SORTIE)
assert PAGES == PAGES_AVANT, (PAGES, PAGES_AVANT)
print('PDF écrit :', SORTIE, '— chapitres aux pages', PAGES)
