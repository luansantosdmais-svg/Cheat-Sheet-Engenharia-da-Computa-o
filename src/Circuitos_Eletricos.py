import math
from pathlib import Path

from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph

OUT = Path('/mnt/data/Circuitos_Eletricos_OneNote.pdf')
PAGE_W, PAGE_H = landscape(A4)
MARGIN = 16

# ---------- fonts ----------
FONT_DIR = Path('/usr/share/fonts/truetype/dejavu')
pdfmetrics.registerFont(TTFont('DVCond', str(FONT_DIR / 'DejaVuSansCondensed.ttf')))
pdfmetrics.registerFont(TTFont('DVCond-Bold', str(FONT_DIR / 'DejaVuSansCondensed-Bold.ttf')))
pdfmetrics.registerFont(TTFont('DVCond-Oblique', str(FONT_DIR / 'DejaVuSansCondensed-Oblique.ttf')))
pdfmetrics.registerFontFamily(
    'DVCond',
    normal='DVCond',
    bold='DVCond-Bold',
    italic='DVCond-Oblique',
    boldItalic='DVCond-Bold',
)

# ---------- palette ----------
BG = HexColor('#F6F8FB')
GRID = HexColor('#E6EBF3')
INK = HexColor('#1C2B4A')
MUTED = HexColor('#5A6B8C')
WHITE = HexColor('#FFFFFF')
LINE = HexColor('#E7ECF4')
AXIS = HexColor('#D7DEEA')

TEAL, TEAL_T = HexColor('#147D82'), HexColor('#E3F2F1')
AMBER, AMBER_T = HexColor('#C97A1A'), HexColor('#FBEDDD')
BERRY, BERRY_T = HexColor('#A83E63'), HexColor('#F6E4EB')
GREEN, GREEN_T = HexColor('#2F7A4F'), HexColor('#E2F0E7')

CARDS = [
    {
        'title': 'GRANDEZAS, OHM<br/>&amp; ASSOCIAÇÕES',
        'color': TEAL,
        'tint': TEAL_T,
        'kind': 'ohm',
        'idea': 'Relacionar tensão, corrente, resistência e potência nos elementos básicos de um circuito.',
        'formulas': [
            '<b>Corrente:</b> I = ΔQ/Δt',
            '<b>Tensão:</b> V = W/Q',
            '<b>Lei de Ohm:</b> V = R·I',
            '<b>Resistência:</b> R = ρL/A',
            '<b>Potência:</b> P = V·I = I²R = V²/R',
            '<b>Série:</b> R<sub>eq</sub> = R<sub>1</sub> + R<sub>2</sub> + ...',
            '<b>Paralelo:</b> 1/R<sub>eq</sub> = Σ(1/R<sub>i</sub>)',
            '<b>Divisor de tensão:</b> V<sub>k</sub> = V·R<sub>k</sub>/ΣR',
        ],
        'tip': 'Antes das contas, marque polaridades e sentidos de corrente. Se o resultado sair negativo, o sentido real é o oposto ao assumido.',
    },
    {
        'title': 'KIRCHHOFF &amp;<br/>ANÁLISE DE CIRCUITOS',
        'color': AMBER,
        'tint': AMBER_T,
        'kind': 'kirchhoff',
        'idea': 'Aplicar conservação de carga e energia para encontrar correntes e tensões em redes elétricas.',
        'formulas': [
            '<b>LKC:</b> ΣI<sub>entrando</sub> = ΣI<sub>saindo</sub>',
            '<b>LKT:</b> soma algébrica das tensões em uma malha = 0',
            '<b>Nós:</b> escolha um nó de referência (0 V)',
            '<b>Malhas:</b> defina uma corrente por malha e aplique LKT',
            '<b>Superposição:</b> uma fonte independente por vez',
            '<b>Thévenin:</b> circuito equivalente V<sub>Th</sub> em série com R<sub>Th</sub>',
            '<b>Norton:</b> I<sub>N</sub> em paralelo com R<sub>N</sub>; R<sub>N</sub>=R<sub>Th</sub>',
            '<b>Máx. potência:</b> R<sub>L</sub> = R<sub>Th</sub>',
        ],
        'tip': 'Em análise nodal use LKC; em malhas use LKT. Escolher o método certo reduz muito o número de equações.',
    },
    {
        'title': 'CAPACITORES, INDUTORES<br/>&amp; TRANSITÓRIOS',
        'color': BERRY,
        'tint': BERRY_T,
        'kind': 'transitorios',
        'idea': 'Entender armazenamento de energia e respostas temporais de circuitos RC e RL.',
        'formulas': [
            '<b>Capacitor:</b> i<sub>C</sub> = C·dv<sub>C</sub>/dt',
            '<b>Indutor:</b> v<sub>L</sub> = L·di<sub>L</sub>/dt',
            '<b>Energia:</b> W<sub>C</sub> = ½CV²; W<sub>L</sub> = ½LI²',
            '<b>Continuidade:</b> v<sub>C</sub>(0⁺)=v<sub>C</sub>(0⁻)',
            '<b>Continuidade:</b> i<sub>L</sub>(0⁺)=i<sub>L</sub>(0⁻)',
            '<b>RC:</b> τ = R<sub>eq</sub>C',
            '<b>RL:</b> τ = L/R<sub>eq</sub>',
            '<b>1ª ordem:</b> x(t)=x(∞)+[x(0⁺)-x(∞)]e<super>-t/τ</super>',
        ],
        'tip': 'Em t = 0⁺, capacitor não muda tensão instantaneamente e indutor não muda corrente instantaneamente. Essa é a chave dos transitórios.',
    },
    {
        'title': 'CA, IMPEDÂNCIA<br/>&amp; POTÊNCIA',
        'color': GREEN,
        'tint': GREEN_T,
        'kind': 'ca',
        'idea': 'Analisar circuitos senoidais usando fasores, impedâncias e relações de potência em regime permanente.',
        'formulas': [
            '<b>Senoide:</b> v(t)=V<sub>m</sub>cos(ωt+φ)',
            '<b>Valor eficaz:</b> V<sub>rms</sub>=V<sub>m</sub>/√2; I<sub>rms</sub>=I<sub>m</sub>/√2',
            '<b>Impedâncias:</b> Z<sub>R</sub>=R; Z<sub>L</sub>=jωL; Z<sub>C</sub>=1/(jωC)',
            '<b>Lei de Ohm fasorial:</b> V = Z·I',
            '<b>Reatância:</b> X<sub>L</sub>=ωL; X<sub>C</sub>=1/(ωC)',
            '<b>Potência ativa:</b> P = V<sub>rms</sub>I<sub>rms</sub>cosφ',
            '<b>Reativa:</b> Q = V<sub>rms</sub>I<sub>rms</sub>senφ; <b>aparente:</b> S = VI',
            '<b>Fator de potência:</b> FP = cosφ',
        ],
        'tip': 'Indutor atrasa a corrente; capacitor adianta. Em CA, use impedâncias como resistências complexas e mantenha os ângulos dos fasores.',
    },
]

# ---------- layout ----------
CARD_TOP = PAGE_H - 16
CARD_BOTTOM = 16
CARD_H = CARD_TOP - CARD_BOTTOM
GAP = 14
CARD_W = (PAGE_W - 2 * MARGIN - 3 * GAP) / 4

STYLE_TITLE = ParagraphStyle(
    'card_title',
    fontName='DVCond-Bold',
    fontSize=17.2,
    leading=18.6,
    textColor=WHITE,
    alignment=1,
    spaceAfter=0,
)
STYLE_IDEA = ParagraphStyle(
    'idea',
    fontName='DVCond-Oblique',
    fontSize=12.6,
    leading=15.6,
    textColor=MUTED,
)
STYLE_TIP = ParagraphStyle(
    'tip',
    fontName='DVCond',
    fontSize=11.7,
    leading=14.7,
    textColor=INK,
)


def arrow(c, x1, y1, x2, y2, color, width=1.2, head=5):
    c.setStrokeColor(color)
    c.setFillColor(color)
    c.setLineWidth(width)
    c.line(x1, y1, x2, y2)
    ang = math.atan2(y2 - y1, x2 - x1)
    for delta in (2.55, -2.55):
        c.line(x2, y2, x2 + head * math.cos(ang + delta), y2 + head * math.sin(ang + delta))


def axis(c, ox, oy, dw, dh):
    ax_y = oy + dh * 0.12
    c.setStrokeColor(AXIS)
    c.setLineWidth(0.8)
    c.line(ox, ax_y, ox + dw, ax_y)
    c.line(ox + dw * 0.03, oy, ox + dw * 0.03, oy + dh)
    return ax_y




def arc_arrow(c, cx, cy, radius, start_deg, end_deg, color):
    c.setStrokeColor(color)
    c.setLineWidth(1.3)
    path = c.beginPath()
    steps = 24
    points = []
    for i in range(steps + 1):
        angle = math.radians(start_deg + (end_deg - start_deg) * i / steps)
        points.append((cx + radius * math.cos(angle), cy + radius * math.sin(angle)))
    path.moveTo(*points[0])
    for point in points[1:]:
        path.lineTo(*point)
    c.drawPath(path, stroke=1, fill=0)
    x1, y1 = points[-2]
    x2, y2 = points[-1]
    arrow(c, x1, y1, x2, y2, color, 1.2, 4.2)

def diagram_ohm(c, ox, oy, dw, dh, color):
    y = oy + dh*0.58
    x0 = ox + dw*0.10
    x1 = ox + dw*0.90
    c.setStrokeColor(INK); c.setLineWidth(1.0)
    c.line(x0, y, x0+24, y)
    # resistor zigzag
    pts=[(x0+24,y),(x0+36,y+9),(x0+48,y-9),(x0+60,y+9),(x0+72,y-9),(x0+84,y)]
    p=c.beginPath(); p.moveTo(*pts[0])
    for pt in pts[1:]: p.lineTo(*pt)
    c.setStrokeColor(color); c.setLineWidth(1.5); c.drawPath(p,stroke=1,fill=0)
    c.setStrokeColor(INK); c.line(x0+84,y,x1,y)
    arrow(c, x0+4, y+20, x1-4, y+20, color, 1.0, 4)
    c.setFillColor(INK); c.setFont('DVCond-Bold',10.2)
    c.drawCentredString((x0+x1)/2, oy+dh*0.16, 'V = R·I   •   P = V·I')
    c.setFillColor(color); c.drawCentredString((x0+x1)/2, y+28, 'I')


def diagram_kirchhoff(c, ox, oy, dw, dh, color):
    # simple two-loop circuit
    x0=ox+dw*0.13; x1=ox+dw*0.87; y0=oy+dh*0.28; y1=oy+dh*0.75; xm=(x0+x1)/2
    c.setStrokeColor(INK); c.setLineWidth(1.1)
    c.rect(x0,y0,x1-x0,y1-y0,stroke=1,fill=0)
    c.line(xm,y0,xm,y1)
    # resistors as small boxes
    for x,y,w,h in [(x0+24,y1-5,28,10),(x1-52,y1-5,28,10),(xm-5,y0+18,10,28)]:
        c.setFillColor(HexColor('#F8FAFD')); c.setStrokeColor(color); c.rect(x,y,w,h,stroke=1,fill=1)
    c.setFillColor(color); c.setFont('DVCond-Bold',9.6)
    c.drawString(x0+28,y1+8,'R₁'); c.drawString(x1-49,y1+8,'R₂'); c.drawString(xm+9,y0+27,'R₃')
    arc_arrow(c,x0+58,(y0+y1)/2,22,205,490,color)
    arc_arrow(c,x1-58,(y0+y1)/2,22,205,490,color)
    c.setFillColor(INK); c.setFont('DVCond-Bold',10.2)
    c.drawCentredString((x0+x1)/2, oy+dh*0.10, 'ΣI = 0   •   ΣV = 0')


def diagram_transitorios(c, ox, oy, dw, dh, color):
    # exponential charge/discharge
    ax=axis(c,ox,oy,dw,dh)
    x0=ox+dw*0.08; x1=ox+dw*0.94
    p=c.beginPath(); p.moveTo(x0,ax+2)
    p.curveTo(x0+dw*0.18,ax+dh*0.50,x0+dw*0.48,ax+dh*0.68,x1,ax+dh*0.72)
    c.setStrokeColor(color); c.setLineWidth(1.6); c.drawPath(p,stroke=1,fill=0)
    p2=c.beginPath(); p2.moveTo(x0,ax+dh*0.72)
    p2.curveTo(x0+dw*0.18,ax+dh*0.28,x0+dw*0.48,ax+dh*0.08,x1,ax+2)
    c.setStrokeColor(INK); c.setLineWidth(1.0); c.drawPath(p2,stroke=1,fill=0)
    tau=x0+dw*0.32; c.setDash([2,2]); c.setStrokeColor(MUTED); c.line(tau,ax,tau,ax+dh*0.50); c.setDash([])
    c.setFillColor(MUTED); c.setFont('DVCond-Bold',9.6); c.drawCentredString(tau,oy+2,'τ')
    c.setFillColor(INK); c.setFont('DVCond-Bold',10.2); c.drawCentredString((x0+x1)/2,oy+dh*0.82,'RC / RL: resposta exponencial')


def diagram_ca(c, ox, oy, dw, dh, color):
    ax=axis(c,ox,oy,dw,dh)
    # sine wave
    p=c.beginPath(); pts=[]
    for i in range(61):
        t=i/60; x=ox+dw*(0.06+0.88*t); y=ax+dh*(0.42+0.26*math.sin(2*math.pi*1.2*t))
        pts.append((x,y))
    p.moveTo(*pts[0])
    for pt in pts[1:]: p.lineTo(*pt)
    c.setStrokeColor(color); c.setLineWidth(1.6); c.drawPath(p,stroke=1,fill=0)
    # phasors
    cx=ox+dw*0.75; cy=oy+dh*0.70
    arrow(c,cx,cy,cx+30,cy,color,1.1,4)
    arrow(c,cx,cy,cx+18,cy+24,INK,1.1,4)
    c.setFillColor(INK); c.setFont('DVCond-Bold',10.0); c.drawCentredString(ox+dw*0.40,oy+dh*0.12,'Z = R + jX   •   V = Z·I')


DIAGRAMS = {
    'ohm': diagram_ohm,
    'kirchhoff': diagram_kirchhoff,
    'transitorios': diagram_transitorios,
    'ca': diagram_ca,
}


def draw_card(c, card, cx):
    color, tint = card['color'], card['tint']

    c.setFillColor(WHITE)
    c.setStrokeColor(color)
    c.setLineWidth(1.5)
    c.roundRect(cx, CARD_BOTTOM, CARD_W, CARD_H, 10, fill=1, stroke=1)

    header_h = 58
    header_y = CARD_TOP - 7 - header_h
    c.setFillColor(color)
    c.roundRect(cx + 5, header_y, CARD_W - 10, header_h, 6, fill=1, stroke=0)
    title = Paragraph(card['title'], STYLE_TITLE)
    _, title_h = title.wrapOn(c, CARD_W - 22, header_h - 6)
    title.drawOn(c, cx + 11, header_y + (header_h - title_h) / 2)

    cursor = header_y - 11

    diagram_h = 76
    diagram_y = cursor - diagram_h
    DIAGRAMS[card['kind']](c, cx + 11, diagram_y, CARD_W - 22, diagram_h, color)
    cursor = diagram_y - 10

    idea = Paragraph(card['idea'], STYLE_IDEA)
    _, idea_h = idea.wrapOn(c, CARD_W - 22, 70)
    idea.drawOn(c, cx + 11, cursor - idea_h)
    cursor -= idea_h + 9

    c.setStrokeColor(LINE)
    c.setLineWidth(0.8)
    c.line(cx + 11, cursor, cx + CARD_W - 11, cursor)
    cursor -= 10

    tip_y = CARD_BOTTOM + 8
    tip = Paragraph('<b>Dica:</b> ' + card['tip'], STYLE_TIP)
    _, tip_text_h = tip.wrapOn(c, CARD_W - 34, 130)
    tip_h = max(72, tip_text_h + 22)
    tip_top = tip_y + tip_h

    formula_html = '<br/>'.join('• ' + item for item in card['formulas'])
    available_h = cursor - tip_top - 10
    font_size = 11.15
    leading = 14.15
    while True:
        style_formula = ParagraphStyle(
            'formula_' + card['kind'],
            fontName='DVCond',
            fontSize=font_size,
            leading=leading,
            textColor=INK,
        )
        formulas = Paragraph(formula_html, style_formula)
        _, formula_h = formulas.wrapOn(c, CARD_W - 22, 470)
        if formula_h <= available_h or font_size <= 10.2:
            break
        font_size -= 0.1
        leading -= 0.1

    formulas.drawOn(c, cx + 11, cursor - formula_h)

    c.setFillColor(tint)
    c.roundRect(cx + 7, tip_y, CARD_W - 14, tip_h, 6, fill=1, stroke=0)
    tip.drawOn(c, cx + 17, tip_y + (tip_h - tip_text_h) / 2)


c = canvas.Canvas(str(OUT), pagesize=landscape(A4))
c.setTitle('Circuitos Elétricos - Cheat Sheet OneNote')
c.setAuthor('OpenAI')

# Background grid
c.setFillColor(BG)
c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
c.setStrokeColor(GRID)
c.setLineWidth(0.35)
step = 16
x = 0
while x < PAGE_W:
    c.line(x, 0, x, PAGE_H)
    x += step
y = 0
while y < PAGE_H:
    c.line(0, y, PAGE_W, y)
    y += step

x = MARGIN
for card in CARDS:
    draw_card(c, card, x)
    x += CARD_W + GAP

c.save()
print(f'PDF gerado em {OUT}')
