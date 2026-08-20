import math
from pathlib import Path
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph

OUT=Path('/mnt/data/Desenvolvimento_em_Javascript_OneNote.pdf')
PAGE_W,PAGE_H=landscape(A4); MARGIN=16
FONT_DIR=Path('/usr/share/fonts/truetype/dejavu')
pdfmetrics.registerFont(TTFont('DVCond',str(FONT_DIR/'DejaVuSansCondensed.ttf')))
pdfmetrics.registerFont(TTFont('DVCond-Bold',str(FONT_DIR/'DejaVuSansCondensed-Bold.ttf')))
pdfmetrics.registerFont(TTFont('DVCond-Oblique',str(FONT_DIR/'DejaVuSansCondensed-Oblique.ttf')))
pdfmetrics.registerFontFamily('DVCond',normal='DVCond',bold='DVCond-Bold',italic='DVCond-Oblique',boldItalic='DVCond-Bold')
BG=HexColor('#F6F8FB'); GRID=HexColor('#E6EBF3'); INK=HexColor('#1C2B4A'); MUTED=HexColor('#5A6B8C'); WHITE=HexColor('#FFFFFF'); LINE=HexColor('#E7ECF4')
TEAL,TEAL_T=HexColor('#147D82'),HexColor('#E3F2F1'); AMBER,AMBER_T=HexColor('#C97A1A'),HexColor('#FBEDDD'); BERRY,BERRY_T=HexColor('#A83E63'),HexColor('#F6E4EB'); GREEN,GREEN_T=HexColor('#2F7A4F'),HexColor('#E2F0E7')

CARDS=[
{'title':'FUNDAMENTOS,<br/>TIPOS &amp; CONTROLE','color':TEAL,'tint':TEAL_T,'kind':'fundamentos','idea':'Dominar a sintaxe essencial, tipos de dados e fluxo de execução antes de construir aplicações maiores.','formulas':['<b>Declaração:</b> const para referência fixa; let para valor mutável','<b>Tipos:</b> string, number, boolean, undefined, null, bigint, symbol','<b>Comparação:</b> prefira === e !== para evitar coerção implícita','<b>Controle:</b> if/else, switch e operador ternário','<b>Laços:</b> for, while, for...of; use break/continue quando necessário','<b>Escopo:</b> let/const respeitam bloco; var possui escopo de função','<b>Truthy/Falsy:</b> cuidado com 0, "", null, undefined, NaN e false'],'tip':'Use const por padrão e mude para let somente quando precisar reatribuir. Prefira === para reduzir comportamentos inesperados.'},
{'title':'FUNÇÕES, ARRAYS<br/>&amp; OBJETOS','color':AMBER,'tint':AMBER_T,'kind':'dados','idea':'Organizar comportamento e dados com funções reutilizáveis, coleções e objetos.','formulas':['<b>Função:</b> parâmetros → processamento → retorno','<b>Arrow:</b> (x) =&gt; x*2; não possui seu próprio this','<b>Array:</b> push/pop; map, filter, find, reduce e forEach','<b>Objeto:</b> pares chave: valor; acesso obj.campo ou obj["campo"]','<b>Desestruturação:</b> const {nome} = pessoa; const [a,b] = lista','<b>Spread:</b> {...obj} e [...arr] criam cópias rasas/combinações','<b>Rest:</b> (...args) agrupa argumentos restantes','<b>Imutabilidade:</b> evite alterar dados compartilhados sem necessidade'],'tip':'map transforma, filter seleciona e reduce acumula. Escolher o método certo deixa o código menor e mais legível.'},
{'title':'DOM, EVENTOS<br/>&amp; ASSÍNCRONO','color':BERRY,'tint':BERRY_T,'kind':'dom','idea':'Conectar JavaScript à interface do navegador e lidar com tarefas que terminam no futuro.','formulas':['<b>DOM:</b> document.querySelector() localiza elementos','<b>Conteúdo:</b> textContent; classes via classList; atributos via setAttribute','<b>Eventos:</b> addEventListener("click", callback)','<b>Event:</b> target identifica origem; preventDefault() cancela comportamento padrão','<b>Promise:</b> representa operação pendente, resolvida ou rejeitada','<b>async/await:</b> sintaxe legível sobre Promises','<b>Fetch:</b> const r = await fetch(url); const data = await r.json()','<b>Erros:</b> try/catch em operações assíncronas que podem falhar'],'tip':'Não bloqueie a interface esperando rede ou timer. Use async/await e sempre trate erros de requisições externas.'},
{'title':'ES6+, MÓDULOS<br/>&amp; BOAS PRÁTICAS','color':GREEN,'tint':GREEN_T,'kind':'modulos','idea':'Estruturar projetos modernos com módulos, classes, tratamento de erros e código fácil de manter.','formulas':['<b>Módulos:</b> export / import separam responsabilidades','<b>Classes:</b> constructor, métodos, extends e super','<b>Optional chaining:</b> obj?.perfil?.nome evita acesso inválido','<b>Nullish:</b> valor ?? padrão usa fallback só para null/undefined','<b>Template string:</b> `Olá ${nome}` para interpolação','<b>JSON:</b> JSON.stringify() e JSON.parse()','<b>Qualidade:</b> funções pequenas, nomes claros, testes e linting'],'tip':'Separe UI, regra de negócio e acesso a dados. Módulos pequenos e previsíveis tornam testes, manutenção e evolução muito mais simples.'}
]

CARD_TOP=PAGE_H-16; CARD_BOTTOM=16; CARD_H=CARD_TOP-CARD_BOTTOM; GAP=14; CARD_W=(PAGE_W-2*MARGIN-3*GAP)/4
STYLE_TITLE=ParagraphStyle('title',fontName='DVCond-Bold',fontSize=17.2,leading=18.6,textColor=WHITE,alignment=1)
STYLE_IDEA=ParagraphStyle('idea',fontName='DVCond-Oblique',fontSize=12.6,leading=15.6,textColor=MUTED)
STYLE_TIP=ParagraphStyle('tip',fontName='DVCond',fontSize=11.7,leading=14.7,textColor=INK)

def arrow(c,x1,y1,x2,y2,color,width=1.1,head=4):
    c.setStrokeColor(color); c.setFillColor(color); c.setLineWidth(width); c.line(x1,y1,x2,y2); a=math.atan2(y2-y1,x2-x1)
    for d in (2.55,-2.55): c.line(x2,y2,x2+head*math.cos(a+d),y2+head*math.sin(a+d))

def box(c,x,y,w,h,color,label):
    c.setStrokeColor(color); c.setFillColor(HexColor('#F8FAFD')); c.setLineWidth(1.1); c.roundRect(x,y,w,h,3,fill=1,stroke=1); c.setFillColor(INK); c.setFont('DVCond-Bold',7.8); c.drawCentredString(x+w/2,y+h/2-3,label)

def diagram_fundamentos(c,ox,oy,dw,dh,color):
    labels=['const','let','if','for']; xs=[ox+dw*.05,ox+dw*.28,ox+dw*.51,ox+dw*.74]; y=oy+dh*.49
    for x,l in zip(xs,labels): box(c,x,y,34,18,color,l)
    for i in range(3): arrow(c,xs[i]+34,y+9,xs[i+1]-4,y+9,color,1.0,3.2)
    c.setFillColor(MUTED); c.setFont('DVCond-Bold',8.7); c.drawCentredString(ox+dw*.5,oy+dh*.18,'dados  →  decisão  →  repetição')

def diagram_dados(c,ox,oy,dw,dh,color):
    # function input/output
    box(c,ox+dw*.08,oy+dh*.50,34,18,color,'x')
    box(c,ox+dw*.36,oy+dh*.45,52,28,color,'função')
    box(c,ox+dw*.74,oy+dh*.50,34,18,color,'y')
    arrow(c,ox+dw*.08+34,oy+dh*.59,ox+dw*.36-4,oy+dh*.59,color,1.0,3.2)
    arrow(c,ox+dw*.36+52,oy+dh*.59,ox+dw*.74-4,oy+dh*.59,color,1.0,3.2)
    # array below
    ax=ox+dw*.20; ay=oy+dh*.16
    for i in range(4):
        c.setStrokeColor(color); c.rect(ax+i*24,ay,20,14,stroke=1,fill=0)
    c.setFillColor(MUTED); c.setFont('DVCond-Bold',8.2); c.drawCentredString(ox+dw*.5,ay-9,'array  +  objeto')

def diagram_dom(c,ox,oy,dw,dh,color):
    box(c,ox+dw*.08,oy+dh*.52,48,20,color,'HTML')
    box(c,ox+dw*.39,oy+dh*.52,48,20,color,'DOM')
    box(c,ox+dw*.70,oy+dh*.52,48,20,color,'JS')
    arrow(c,ox+dw*.08+48,oy+dh*.62,ox+dw*.39-4,oy+dh*.62,color,1.0,3.2)
    arrow(c,ox+dw*.39+48,oy+dh*.62,ox+dw*.70-4,oy+dh*.62,color,1.0,3.2)
    # async timeline
    y=oy+dh*.20; c.setStrokeColor(color); c.line(ox+dw*.14,y,ox+dw*.84,y); arrow(c,ox+dw*.14,y,ox+dw*.84,y,color,1.0,3.2)
    for frac,label in [(0.25,'fetch'),(0.55,'await'),(0.78,'data')]:
        x=ox+dw*frac; c.circle(x,y,3.5,stroke=1,fill=0); c.setFillColor(INK); c.setFont('DVCond-Bold',7.2); c.drawCentredString(x,y+9,label)

def diagram_modulos(c,ox,oy,dw,dh,color):
    box(c,ox+dw*.08,oy+dh*.50,46,20,color,'UI')
    box(c,ox+dw*.38,oy+dh*.50,58,20,color,'Lógica')
    box(c,ox+dw*.74,oy+dh*.50,46,20,color,'Dados')
    arrow(c,ox+dw*.08+46,oy+dh*.60,ox+dw*.38-4,oy+dh*.60,color,1.0,3.2)
    arrow(c,ox+dw*.38+58,oy+dh*.60,ox+dw*.74-4,oy+dh*.60,color,1.0,3.2)
    c.setFillColor(INK); c.setFont('DVCond-Bold',9); c.drawCentredString(ox+dw*.50,oy+dh*.19,'export  •  import  •  testes')

DIAGRAMS={'fundamentos':diagram_fundamentos,'dados':diagram_dados,'dom':diagram_dom,'modulos':diagram_modulos}

def draw_card(c,card,cx):
    color,tint=card['color'],card['tint']; c.setFillColor(WHITE); c.setStrokeColor(color); c.setLineWidth(1.5); c.roundRect(cx,CARD_BOTTOM,CARD_W,CARD_H,10,fill=1,stroke=1)
    hh=58; hy=CARD_TOP-7-hh; c.setFillColor(color); c.roundRect(cx+5,hy,CARD_W-10,hh,6,fill=1,stroke=0)
    p=Paragraph(card['title'],STYLE_TITLE); _,ph=p.wrapOn(c,CARD_W-22,hh-6); p.drawOn(c,cx+11,hy+(hh-ph)/2)
    cursor=hy-11; dh=76; dy=cursor-dh; DIAGRAMS[card['kind']](c,cx+11,dy,CARD_W-22,dh,color); cursor=dy-10
    p=Paragraph(card['idea'],STYLE_IDEA); _,ph=p.wrapOn(c,CARD_W-22,70); p.drawOn(c,cx+11,cursor-ph); cursor-=ph+9
    c.setStrokeColor(LINE); c.setLineWidth(.8); c.line(cx+11,cursor,cx+CARD_W-11,cursor); cursor-=10
    tip_y=CARD_BOTTOM+8; tip=Paragraph('<b>Dica:</b> '+card['tip'],STYLE_TIP); _,th=tip.wrapOn(c,CARD_W-34,130); tip_h=max(72,th+22); tip_top=tip_y+tip_h
    html='<br/>'.join('• '+x for x in card['formulas']); available=cursor-tip_top-10; fs=10.7; lead=13.7
    while True:
        st=ParagraphStyle('b_'+card['kind'],fontName='DVCond',fontSize=fs,leading=lead,textColor=INK); body=Paragraph(html,st); _,bh=body.wrapOn(c,CARD_W-22,470)
        if bh<=available or fs<=9.9: break
        fs-=.1; lead-=.1
    body.drawOn(c,cx+11,cursor-bh)
    c.setFillColor(tint); c.roundRect(cx+7,tip_y,CARD_W-14,tip_h,6,fill=1,stroke=0); tip.drawOn(c,cx+17,tip_y+(tip_h-th)/2)

c=canvas.Canvas(str(OUT),pagesize=landscape(A4)); c.setTitle('Desenvolvimento em JavaScript - Cheat Sheet OneNote'); c.setAuthor('OpenAI')
c.setFillColor(BG); c.rect(0,0,PAGE_W,PAGE_H,fill=1,stroke=0); c.setStrokeColor(GRID); c.setLineWidth(.35)
step=16; x=0
while x<PAGE_W: c.line(x,0,x,PAGE_H); x+=step
y=0
while y<PAGE_H: c.line(0,y,PAGE_W,y); y+=step
x=MARGIN
for card in CARDS: draw_card(c,card,x); x+=CARD_W+GAP
c.save(); print(OUT)
