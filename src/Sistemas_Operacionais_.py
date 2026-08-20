import math
from pathlib import Path

from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph

OUT = Path('/mnt/data/Sistemas_Operacionais_OneNote_Vetor.pdf')
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
        'title': 'PROCESSOS &amp;<br/>THREADS',
        'color': TEAL,
        'tint': TEAL_T,
        'kind': 'processos',
        'idea': 'Entender execução concorrente, estados e como processos e threads usam recursos do sistema.',
        'formulas': [
            '<b>Processo:</b> programa em execução com recursos próprios',
            '<b>Estados:</b> novo, pronto, executando, espera e terminado',
            '<b>PCB:</b> PID + registradores + estado + contador de programa',
            '<b>Thread:</b> unidade de execução dentro de um processo',
            '<b>Compartilhamento:</b> threads dividem código, dados e arquivos',
            '<b>Pilha:</b> cada thread possui sua própria pilha',
            '<b>Troca de contexto:</b> salva estado atual e restaura o próximo',
            '<b>Processo × thread:</b> processo isola memória; thread é mais leve',
        ],
        'tip': 'Processo tem espaço de endereçamento próprio; threads do mesmo processo compartilham memória e recursos.',
    },
    {
        'title': 'ESCALONAMENTO &amp;<br/>SINCRONIZAÇÃO',
        'color': AMBER,
        'tint': AMBER_T,
        'kind': 'escalonamento',
        'idea': 'Distribuir CPU entre tarefas e proteger recursos compartilhados contra acessos incorretos.',
        'formulas': [
            '<b>Objetivo:</b> melhorar utilização da CPU e tempo de resposta',
            '<b>FCFS:</b> primeiro a chegar, primeiro a ser atendido',
            '<b>SJF:</b> menor trabalho primeiro',
            '<b>Prioridade:</b> maior prioridade executa antes',
            '<b>Round Robin:</b> cada processo recebe um quantum',
            '<b>Preemptivo:</b> SO pode interromper a execução',
            '<b>Seção crítica:</b> trecho que acessa recurso compartilhado',
            '<b>Sincronização:</b> mutex e semáforos evitam race conditions',
            '<b>Deadlock:</b> exclusão mútua + posse/espera + não preempção + ciclo',
        ],
        'tip': 'Round Robin é clássico em time-sharing. Quantum muito pequeno aumenta o overhead de troca de contexto.',
    },
    {
        'title': 'MEMÓRIA &amp;<br/>MEMÓRIA VIRTUAL',
        'color': BERRY,
        'tint': BERRY_T,
        'kind': 'memoria',
        'idea': 'Mapear endereços e usar paginação para ampliar a memória disponível ao processo.',
        'formulas': [
            '<b>Endereço lógico:</b> gerado pelo processo',
            '<b>Endereço físico:</b> posição real na RAM',
            '<b>Paginação:</b> memória lógica em páginas e física em quadros',
            '<b>Tabela de páginas:</b> mapeia página lógica → quadro físico',
            '<b>Fragmentação interna:</b> sobra dentro de um quadro',
            '<b>Memória virtual:</b> usa disco para ampliar a memória aparente',
            '<b>Page fault:</b> página necessária não está na RAM',
            '<b>Substituição:</b> FIFO, LRU e Ótimo (conceitual)',
            '<b>Thrashing:</b> excesso de page faults e pouca execução útil',
        ],
        'tip': 'Muitos page faults seguidos podem indicar thrashing: o sistema passa mais tempo trocando páginas do que executando.',
    },
    {
        'title': 'ARQUIVOS, E/S<br/>&amp; PROTEÇÃO',
        'color': GREEN,
        'tint': GREEN_T,
        'kind': 'arquivos',
        'idea': 'Organizar armazenamento, controlar dispositivos e proteger o acesso aos recursos do sistema.',
        'formulas': [
            '<b>Arquivo:</b> conjunto ordenado de bytes com nome e metadados',
            '<b>Diretórios:</b> organizam arquivos de forma hierárquica',
            '<b>Operações:</b> abrir, ler, escrever, fechar, criar e deletar',
            '<b>E/S:</b> pode usar interrupção, polling ou DMA',
            '<b>DMA:</b> transferência direta entre dispositivo e memória',
            '<b>Proteção:</b> usuários, permissões e modos de acesso',
            '<b>Modo usuário:</b> restrito; <b>modo kernel:</b> privilegiado',
            '<b>Syscall:</b> interface controlada entre aplicação e kernel',
            '<b>Kernel:</b> gerencia recursos com segurança e eficiência',
        ],
        'tip': 'Syscall é a ponte controlada entre programas em modo usuário e os serviços privilegiados oferecidos pelo kernel.',
    },
]

# ---------- layout ----------
CARD_TOP = PAGE_H - 16
CARD_BOTTOM = 16
CARD_H = CARD_TOP - CARD_BOTTOM
GAP = 14
CARD_W = (PAGE_W - 2 * MARGIN - 3 * GAP) / 4

STYLE_TITLE = ParagraphStyle(
    'card_title', fontName='DVCond-Bold', fontSize=17.2, leading=18.6,
    textColor=WHITE, alignment=1
)
STYLE_IDEA = ParagraphStyle(
    'idea', fontName='DVCond-Oblique', fontSize=12.6, leading=15.6,
    textColor=MUTED
)
STYLE_TIP = ParagraphStyle(
    'tip', fontName='DVCond', fontSize=11.7, leading=14.7,
    textColor=INK
)


def arrow(c, x1, y1, x2, y2, color, width=1.2, head=4.5):
    c.setStrokeColor(color)
    c.setFillColor(color)
    c.setLineWidth(width)
    c.line(x1, y1, x2, y2)
    ang = math.atan2(y2-y1, x2-x1)
    for delta in (2.55, -2.55):
        c.line(x2, y2, x2 + head*math.cos(ang+delta), y2 + head*math.sin(ang+delta))


def small_box(c, x, y, w, h, color, label, fs=8.0):
    c.setStrokeColor(color)
    c.setFillColor(HexColor('#F8FAFD'))
    c.setLineWidth(1.1)
    c.roundRect(x, y, w, h, 3, fill=1, stroke=1)
    c.setFillColor(INK)
    c.setFont('DVCond-Bold', fs)
    c.drawCentredString(x+w/2, y+h/2-3, label)


def diagram_processos(c, ox, oy, dw, dh, color):
    py = oy + dh*0.58
    small_box(c, ox+dw*0.02, py, 48, 26, color, 'Processo')
    arrow(c, ox+dw*0.28, py+13, ox+dw*0.42, py+13, color, 1.0, 4)
    c.setFillColor(color)
    c.setFont('DVCond-Bold', 8)
    c.drawCentredString(ox+dw*0.35, py+23, 'cria')
    # threads
    for i in range(3):
        x = ox + dw*(0.56 + 0.13*i)
        path = c.beginPath()
        path.moveTo(x, py+2)
        path.curveTo(x-5, py+8, x+5, py+13, x, py+19)
        path.curveTo(x-5, py+23, x+5, py+28, x, py+34)
        c.setStrokeColor(color)
        c.setLineWidth(1.0)
        c.drawPath(path, stroke=1, fill=0)
    c.setFillColor(color)
    c.setFont('DVCond-Bold', 7.5)
    c.drawCentredString(ox+dw*0.73, py+39, 'Threads T1 T2 T3')
    # states
    y = oy + dh*0.20
    xs = [ox+dw*0.08, ox+dw*0.34, ox+dw*0.60, ox+dw*0.84]
    labs = ['Novo', 'Pronto', 'Exec.', 'Espera']
    for x, lab in zip(xs, labs):
        c.setStrokeColor(color)
        c.setLineWidth(1.0)
        c.circle(x, y, 13, stroke=1, fill=0)
        c.setFillColor(INK)
        c.setFont('DVCond-Bold', 7.2)
        c.drawCentredString(x, y-2.5, lab)
    for a,b in zip(xs[:-1], xs[1:]):
        arrow(c, a+14, y, b-14, y, color, 0.9, 3.6)
    arrow(c, xs[3], y-14, xs[1], y-14, color, 0.8, 3.2)


def diagram_escalonamento(c, ox, oy, dw, dh, color):
    # ready queue
    qx, qy = ox+dw*0.06, oy+dh*0.60
    c.setFillColor(color)
    c.setFont('DVCond-Bold', 8)
    c.drawString(qx, qy+22, 'Fila de prontos')
    for i in range(4):
        c.setStrokeColor(color)
        c.rect(qx+i*24, qy, 22, 18, stroke=1, fill=0)
    arrow(c, qx+100, qy+9, ox+dw*0.78, qy+9, color, 1.0, 4)
    c.setStrokeColor(color)
    c.circle(ox+dw*0.88, qy+9, 15, stroke=1, fill=0)
    c.setFillColor(INK)
    c.setFont('DVCond-Bold', 8.3)
    c.drawCentredString(ox+dw*0.88, qy+6, 'CPU')
    # mutex
    y = oy+dh*0.21
    small_box(c, ox+dw*0.08, y, 42, 18, color, 'Thread A', 7.2)
    small_box(c, ox+dw*0.70, y, 42, 18, color, 'Thread B', 7.2)
    lx = ox+dw*0.50
    c.setStrokeColor(INK)
    c.setLineWidth(1.0)
    c.roundRect(lx-7, y+1, 14, 14, 2, stroke=1, fill=0)
    c.arc(lx-6, y+10, lx+6, y+24, 0, 180)
    c.setDash([2,2])
    c.line(ox+dw*0.08+42, y+9, lx-9, y+9)
    c.line(lx+9, y+9, ox+dw*0.70, y+9)
    c.setDash([])
    c.setFillColor(color)
    c.setFont('DVCond-Bold', 8)
    c.drawCentredString(lx, y+27, 'mutex')


def diagram_memoria(c, ox, oy, dw, dh, color):
    # RAM frames
    x1 = ox+dw*0.06
    y = oy+dh*0.18
    c.setFillColor(color)
    c.setFont('DVCond-Bold', 8)
    c.drawString(x1, oy+dh*0.82, 'RAM')
    for i in range(5):
        c.setStrokeColor(color)
        c.rect(x1, y+i*13, 24, 12, stroke=1, fill=0)
    # pages
    x2 = ox+dw*0.50
    c.setFillColor(color)
    c.setFont('DVCond-Bold', 8)
    c.drawCentredString(x2+16, oy+dh*0.82, 'Páginas')
    for i,lab in enumerate(['P0','P1','P2','P3','Pn']):
        c.setStrokeColor(color)
        c.rect(x2, y+i*13, 32, 12, stroke=1, fill=0)
        c.setFillColor(INK)
        c.setFont('DVCond-Bold', 7)
        c.drawCentredString(x2+16, y+i*13+3, lab)
    # disk
    dx = ox+dw*0.84
    c.setStrokeColor(color)
    c.ellipse(dx-16, y+10, dx+16, y+22, stroke=1, fill=0)
    c.line(dx-16, y+16, dx-16, y+48)
    c.line(dx+16, y+16, dx+16, y+48)
    c.ellipse(dx-16, y+42, dx+16, y+54, stroke=1, fill=0)
    c.setFillColor(color)
    c.setFont('DVCond-Bold', 7.5)
    c.drawCentredString(dx, oy+dh*0.82, 'Swap')
    # map arrows
    c.setDash([2,2])
    arrow(c, x1+28, y+34, x2-5, y+34, INK, 0.8, 3)
    arrow(c, x2+36, y+34, dx-20, y+34, color, 0.8, 3)
    c.setDash([])


def diagram_arquivos(c, ox, oy, dw, dh, color):
    # directory tree
    rootx, rooty = ox+dw*0.24, oy+dh*0.70
    small_box(c, rootx-13, rooty, 26, 15, color, 'dir', 7)
    children = [(ox+dw*0.10, oy+dh*0.43), (ox+dw*0.24, oy+dh*0.43), (ox+dw*0.38, oy+dh*0.43)]
    c.setStrokeColor(color)
    for cx,cy in children:
        c.line(rootx, rooty, cx, cy+15)
        small_box(c, cx-11, cy, 22, 14, color, 'f', 7)
    # I/O flow right
    x = ox+dw*0.62
    ys = [oy+dh*0.69, oy+dh*0.49, oy+dh*0.29, oy+dh*0.09]
    labs = ['Aplicação', 'Kernel', 'Controlador', 'Dispositivo']
    for yy,lab in zip(ys,labs):
        small_box(c, x, yy, 62, 16, color, lab, 7.3)
    for i in range(3):
        arrow(c, x+31, ys[i]-2, x+31, ys[i+1]+18, color, 0.9, 3.5)


DIAGRAMS = {
    'processos': diagram_processos,
    'escalonamento': diagram_escalonamento,
    'memoria': diagram_memoria,
    'arquivos': diagram_arquivos,
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
    c.roundRect(cx+5, header_y, CARD_W-10, header_h, 6, fill=1, stroke=0)
    title = Paragraph(card['title'], STYLE_TITLE)
    _, th = title.wrapOn(c, CARD_W-22, header_h-6)
    title.drawOn(c, cx+11, header_y + (header_h-th)/2)

    cursor = header_y - 11

    diagram_h = 76
    diagram_y = cursor - diagram_h
    DIAGRAMS[card['kind']](c, cx+11, diagram_y, CARD_W-22, diagram_h, color)
    cursor = diagram_y - 10

    idea = Paragraph(card['idea'], STYLE_IDEA)
    _, ih = idea.wrapOn(c, CARD_W-22, 70)
    idea.drawOn(c, cx+11, cursor-ih)
    cursor -= ih + 9

    c.setStrokeColor(LINE)
    c.setLineWidth(0.8)
    c.line(cx+11, cursor, cx+CARD_W-11, cursor)
    cursor -= 10

    tip_y = CARD_BOTTOM + 8
    tip = Paragraph('<b>Dica:</b> ' + card['tip'], STYLE_TIP)
    _, tip_text_h = tip.wrapOn(c, CARD_W-34, 130)
    tip_h = max(72, tip_text_h + 22)
    tip_top = tip_y + tip_h

    body_html = '<br/>'.join('• ' + item for item in card['formulas'])
    available_h = cursor - tip_top - 10
    font_size = 10.7
    leading = 13.55
    while True:
        body_style = ParagraphStyle(
            'body_' + card['kind'],
            fontName='DVCond', fontSize=font_size, leading=leading, textColor=INK
        )
        body = Paragraph(body_html, body_style)
        _, body_h = body.wrapOn(c, CARD_W-22, 470)
        if body_h <= available_h or font_size <= 9.9:
            break
        font_size -= 0.1
        leading -= 0.1
    body.drawOn(c, cx+11, cursor-body_h)

    c.setFillColor(tint)
    c.roundRect(cx+7, tip_y, CARD_W-14, tip_h, 6, fill=1, stroke=0)
    tip.drawOn(c, cx+17, tip_y + (tip_h-tip_text_h)/2)


c = canvas.Canvas(str(OUT), pagesize=landscape(A4))
c.setTitle('Sistemas Operacionais - Cheat Sheet OneNote')
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
