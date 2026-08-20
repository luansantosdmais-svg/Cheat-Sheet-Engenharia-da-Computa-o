import math
from pathlib import Path
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph

OUT = Path('/mnt/data/Linguagem_Orientada_a_Objetos_OneNote.pdf')
PAGE_W, PAGE_H = landscape(A4)
MARGIN = 16

FONT_DIR = Path('/usr/share/fonts/truetype/dejavu')
pdfmetrics.registerFont(TTFont('DVCond', str(FONT_DIR / 'DejaVuSansCondensed.ttf')))
pdfmetrics.registerFont(TTFont('DVCond-Bold', str(FONT_DIR / 'DejaVuSansCondensed-Bold.ttf')))
pdfmetrics.registerFont(TTFont('DVCond-Oblique', str(FONT_DIR / 'DejaVuSansCondensed-Oblique.ttf')))
pdfmetrics.registerFontFamily('DVCond', normal='DVCond', bold='DVCond-Bold', italic='DVCond-Oblique', boldItalic='DVCond-Bold')

BG = HexColor('#F6F8FB'); GRID = HexColor('#E6EBF3'); INK = HexColor('#1C2B4A'); MUTED = HexColor('#5A6B8C')
WHITE = HexColor('#FFFFFF'); LINE = HexColor('#E7ECF4'); AXIS = HexColor('#D7DEEA')
TEAL, TEAL_T = HexColor('#147D82'), HexColor('#E3F2F1')
AMBER, AMBER_T = HexColor('#C97A1A'), HexColor('#FBEDDD')
BERRY, BERRY_T = HexColor('#A83E63'), HexColor('#F6E4EB')
GREEN, GREEN_T = HexColor('#2F7A4F'), HexColor('#E2F0E7')

CARDS = [
    {'title':'CLASSES, OBJETOS<br/>&amp; ENCAPSULAMENTO','color':TEAL,'tint':TEAL_T,'kind':'classes',
     'idea':'Modelar entidades com estado e comportamento, protegendo detalhes internos da implementação.',
     'formulas':['<b>Classe:</b> molde que define atributos e métodos','<b>Objeto:</b> instância concreta criada a partir da classe','<b>Atributo:</b> representa estado/dados do objeto','<b>Método:</b> representa comportamento/operação','<b>Construtor:</b> inicializa o estado do objeto','<b>Encapsulamento:</b> restringe acesso ao estado interno','<b>Visibilidade:</b> public, private, protected','<b>Get/Set:</b> controlam leitura e alteração de atributos'],
     'tip':'Evite deixar atributos públicos sem necessidade. Encapsular permite validar regras e reduzir acoplamento.'},
    {'title':'HERANÇA,<br/>POLIMORFISMO &amp; ABSTRAÇÃO','color':AMBER,'tint':AMBER_T,'kind':'heranca',
     'idea':'Reutilizar comportamento comum e trabalhar com diferentes implementações por uma mesma interface.',
     'formulas':['<b>Herança:</b> classe filha reutiliza/estende a classe base','<b>É-um:</b> relação típica para herança','<b>Sobrescrita:</b> redefinir método herdado','<b>Polimorfismo:</b> mesma chamada, comportamentos diferentes','<b>Classe abstrata:</b> define estrutura comum e pode ter métodos abstratos','<b>Interface:</b> contrato de operações esperadas','<b>Upcasting:</b> tratar objeto filho como tipo pai','<b>Preferência:</b> composição costuma ser mais flexível que herança'],
     'tip':'Use herança quando houver relação “é-um” verdadeira. Para apenas reutilizar funcionalidade, composição costuma ser mais segura.'},
    {'title':'ASSOCIAÇÃO,<br/>COMPOSIÇÃO &amp; UML','color':BERRY,'tint':BERRY_T,'kind':'uml',
     'idea':'Representar como objetos colaboram e como as relações aparecem no modelo orientado a objetos.',
     'formulas':['<b>Associação:</b> objetos conhecem/colaboram entre si','<b>Agregação:</b> relação todo-parte fraca; partes podem existir sozinhas','<b>Composição:</b> todo-parte forte; ciclo de vida das partes depende do todo','<b>Dependência:</b> uso temporário de outra classe','<b>Multiplicidade:</b> 1, 0..1, 1..*, 0..*','<b>UML:</b> classe mostra nome, atributos e operações','<b>Acoplamento:</b> dependência entre classes; quanto menor, melhor','<b>Coesão:</b> foco interno da classe; quanto maior, melhor'],
     'tip':'Em UML, não desenhe relações só por aparência. Cada seta deve representar uma relação real no código ou no domínio.'},
    {'title':'EXCEÇÕES, GENÉRICOS<br/>&amp; BOAS PRÁTICAS','color':GREEN,'tint':GREEN_T,'kind':'boas',
     'idea':'Construir código OO mais reutilizável, robusto e fácil de manter.',
     'formulas':['<b>Exceção:</b> representa situação anormal durante a execução','<b>try/catch/finally:</b> tratar erro e garantir limpeza de recursos','<b>throw:</b> lançar explicitamente uma exceção','<b>Genéricos:</b> reutilizam estruturas com segurança de tipos','<b>SOLID:</b> princípios para reduzir acoplamento e facilitar evolução','<b>SRP:</b> classe deve ter uma responsabilidade principal','<b>OCP:</b> aberto para extensão, fechado para modificação','<b>Boas práticas:</b> nomes claros, métodos curtos, testes e baixo acoplamento'],
     'tip':'OO não é só criar classes. O objetivo é distribuir responsabilidades de forma clara e tornar mudanças futuras menos custosas.'}
]

CARD_TOP = PAGE_H - 16; CARD_BOTTOM = 16; CARD_H = CARD_TOP - CARD_BOTTOM; GAP = 14
CARD_W = (PAGE_W - 2*MARGIN - 3*GAP) / 4
STYLE_TITLE = ParagraphStyle('card_title', fontName='DVCond-Bold', fontSize=17.2, leading=18.6, textColor=WHITE, alignment=1)
STYLE_IDEA = ParagraphStyle('idea', fontName='DVCond-Oblique', fontSize=12.6, leading=15.6, textColor=MUTED)
STYLE_TIP = ParagraphStyle('tip', fontName='DVCond', fontSize=11.7, leading=14.7, textColor=INK)

def arrow(c,x1,y1,x2,y2,color,width=1.1,head=4):
    c.setStrokeColor(color); c.setFillColor(color); c.setLineWidth(width); c.line(x1,y1,x2,y2)
    a=math.atan2(y2-y1,x2-x1)
    for d in (2.55,-2.55): c.line(x2,y2,x2+head*math.cos(a+d),y2+head*math.sin(a+d))

def box(c,x,y,w,h,color,label=None):
    c.setStrokeColor(color); c.setFillColor(HexColor('#F8FAFD')); c.setLineWidth(1.2); c.roundRect(x,y,w,h,3,fill=1,stroke=1)
    if label:
        c.setFillColor(INK); c.setFont('DVCond-Bold',8.4); c.drawCentredString(x+w/2,y+h/2-3,label)

def diagram_classes(c,ox,oy,dw,dh,color):
    x=ox+dw*.15; y=oy+dh*.23; w=dw*.70; h=dh*.56
    c.setStrokeColor(color); c.setFillColor(HexColor('#F8FAFD')); c.setLineWidth(1.2); c.roundRect(x,y,w,h,4,fill=1,stroke=1)
    c.line(x,y+h*.66,x+w,y+h*.66); c.line(x,y+h*.37,x+w,y+h*.37)
    c.setFillColor(color); c.setFont('DVCond-Bold',9.2); c.drawCentredString(x+w/2,y+h-13,'CONTA')
    c.setFillColor(INK); c.setFont('DVCond',7.4); c.drawString(x+8,y+h*.48,'- saldo'); c.drawString(x+8,y+h*.18,'+ depositar()   + sacar()')
    c.setFillColor(MUTED); c.setFont('DVCond-Bold',8.2); c.drawCentredString(x+w/2,oy+dh*.12,'classe  →  objeto')

def diagram_heranca(c,ox,oy,dw,dh,color):
    box(c,ox+dw*.36,oy+dh*.62,70,20,color,'ANIMAL')
    box(c,ox+dw*.12,oy+dh*.24,58,20,color,'CÃO'); box(c,ox+dw*.62,oy+dh*.24,58,20,color,'GATO')
    c.setStrokeColor(color); c.setLineWidth(1.2)
    c.line(ox+dw*.47,oy+dh*.62,ox+dw*.25,oy+dh*.44); c.line(ox+dw*.47,oy+dh*.62,ox+dw*.73,oy+dh*.44)
    c.setFillColor(INK); c.setFont('DVCond-Bold',8.8); c.drawCentredString(ox+dw*.50,oy+dh*.12,'falar() → comportamentos diferentes')

def diagram_uml(c,ox,oy,dw,dh,color):
    box(c,ox+dw*.08,oy+dh*.42,56,26,color,'PEDIDO'); box(c,ox+dw*.68,oy+dh*.42,56,26,color,'ITEM')
    c.setStrokeColor(color); c.setLineWidth(1.2); c.line(ox+dw*.08+56,oy+dh*.55,ox+dw*.68,oy+dh*.55)
    c.setFillColor(color); c.setFont('DVCond-Bold',10); c.drawString(ox+dw*.37,oy+dh*.60,'1'); c.drawString(ox+dw*.58,oy+dh*.60,'*')
    c.setFillColor(INK); c.setFont('DVCond-Bold',8.8); c.drawCentredString(ox+dw*.50,oy+dh*.19,'associação   •   composição')

def diagram_boas(c,ox,oy,dw,dh,color):
    xs=[ox+dw*.06,ox+dw*.29,ox+dw*.52,ox+dw*.75]; labs=['try','catch','T','SOLID']; y=oy+dh*.44
    for x,lab in zip(xs,labs): box(c,x,y,34,18,color,lab)
    for i in range(3): arrow(c,xs[i]+34,y+9,xs[i+1]-4,y+9,color,1.0,3.5)
    c.setFillColor(INK); c.setFont('DVCond-Bold',8.8); c.drawCentredString(ox+dw*.49,oy+dh*.18,'robustez   •   reuso   •   manutenção')

DIAGRAMS={'classes':diagram_classes,'heranca':diagram_heranca,'uml':diagram_uml,'boas':diagram_boas}

def draw_card(c,card,cx):
    color,tint=card['color'],card['tint']
    c.setFillColor(WHITE); c.setStrokeColor(color); c.setLineWidth(1.5); c.roundRect(cx,CARD_BOTTOM,CARD_W,CARD_H,10,fill=1,stroke=1)
    header_h=58; header_y=CARD_TOP-7-header_h
    c.setFillColor(color); c.roundRect(cx+5,header_y,CARD_W-10,header_h,6,fill=1,stroke=0)
    p=Paragraph(card['title'],STYLE_TITLE); _,ph=p.wrapOn(c,CARD_W-22,header_h-6); p.drawOn(c,cx+11,header_y+(header_h-ph)/2)
    cursor=header_y-11; dh=76; dy=cursor-dh; DIAGRAMS[card['kind']](c,cx+11,dy,CARD_W-22,dh,color); cursor=dy-10
    p=Paragraph(card['idea'],STYLE_IDEA); _,ph=p.wrapOn(c,CARD_W-22,70); p.drawOn(c,cx+11,cursor-ph); cursor-=ph+9
    c.setStrokeColor(LINE); c.setLineWidth(.8); c.line(cx+11,cursor,cx+CARD_W-11,cursor); cursor-=10
    tip_y=CARD_BOTTOM+8; tip=Paragraph('<b>Dica:</b> '+card['tip'],STYLE_TIP); _,tip_txt_h=tip.wrapOn(c,CARD_W-34,130); tip_h=max(72,tip_txt_h+22); tip_top=tip_y+tip_h
    html='<br/>'.join('• '+x for x in card['formulas']); available=cursor-tip_top-10; fs=10.85; lead=13.75
    while True:
        st=ParagraphStyle('body_'+card['kind'],fontName='DVCond',fontSize=fs,leading=lead,textColor=INK); body=Paragraph(html,st); _,bh=body.wrapOn(c,CARD_W-22,470)
        if bh<=available or fs<=9.95: break
        fs-=.1; lead-=.1
    body.drawOn(c,cx+11,cursor-bh)
    c.setFillColor(tint); c.roundRect(cx+7,tip_y,CARD_W-14,tip_h,6,fill=1,stroke=0); tip.drawOn(c,cx+17,tip_y+(tip_h-tip_txt_h)/2)

c=canvas.Canvas(str(OUT),pagesize=landscape(A4)); c.setTitle('Linguagem Orientada a Objetos - Cheat Sheet OneNote'); c.setAuthor('OpenAI')
c.setFillColor(BG); c.rect(0,0,PAGE_W,PAGE_H,fill=1,stroke=0); c.setStrokeColor(GRID); c.setLineWidth(.35)
step=16; x=0
while x<PAGE_W: c.line(x,0,x,PAGE_H); x+=step
y=0
while y<PAGE_H: c.line(0,y,PAGE_W,y); y+=step
x=MARGIN
for card in CARDS: draw_card(c,card,x); x+=CARD_W+GAP
c.save(); print(OUT)
