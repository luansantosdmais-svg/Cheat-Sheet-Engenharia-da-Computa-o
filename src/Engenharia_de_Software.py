import math
from pathlib import Path
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph

OUT=Path('/mnt/data/Engenharia_de_Software_OneNote.pdf')
PAGE_W,PAGE_H=landscape(A4); MARGIN=16
FONT_DIR=Path('/usr/share/fonts/truetype/dejavu')
pdfmetrics.registerFont(TTFont('DVCond',str(FONT_DIR/'DejaVuSansCondensed.ttf')))
pdfmetrics.registerFont(TTFont('DVCond-Bold',str(FONT_DIR/'DejaVuSansCondensed-Bold.ttf')))
pdfmetrics.registerFont(TTFont('DVCond-Oblique',str(FONT_DIR/'DejaVuSansCondensed-Oblique.ttf')))
pdfmetrics.registerFontFamily('DVCond',normal='DVCond',bold='DVCond-Bold',italic='DVCond-Oblique',boldItalic='DVCond-Bold')
BG=HexColor('#F6F8FB'); GRID=HexColor('#E6EBF3'); INK=HexColor('#1C2B4A'); MUTED=HexColor('#5A6B8C'); WHITE=HexColor('#FFFFFF'); LINE=HexColor('#E7ECF4')
TEAL,TEAL_T=HexColor('#147D82'),HexColor('#E3F2F1'); AMBER,AMBER_T=HexColor('#C97A1A'),HexColor('#FBEDDD'); BERRY,BERRY_T=HexColor('#A83E63'),HexColor('#F6E4EB'); GREEN,GREEN_T=HexColor('#2F7A4F'),HexColor('#E2F0E7')

CARDS=[
{'title':'PROCESSOS &amp;<br/>CICLO DE VIDA','color':TEAL,'tint':TEAL_T,'kind':'processos','idea':'Organizar o desenvolvimento em etapas, artefatos e ciclos de feedback para entregar software com previsibilidade.','formulas':['<b>Ciclo de vida:</b> requisitos → projeto → código → testes → manutenção','<b>Cascata:</b> etapas sequenciais; mudanças tardias custam mais','<b>Incremental:</b> entrega em partes funcionais','<b>Iterativo:</b> refina a solução em ciclos','<b>Ágil:</b> entregas frequentes + adaptação','<b>Scrum:</b> Backlog, Sprint, Review e Retrospective','<b>Kanban:</b> fluxo visual, limite de WIP e melhoria contínua','<b>DevOps:</b> integra dev, operações e automação'],'tip':'Processo não é burocracia por si só. O objetivo é reduzir risco, dar visibilidade e criar feedback rápido para corrigir o rumo cedo.'},
{'title':'REQUISITOS,<br/>UML &amp; MODELAGEM','color':AMBER,'tint':AMBER_T,'kind':'requisitos','idea':'Entender o problema antes de codificar, registrando comportamento, regras e estrutura do sistema.','formulas':['<b>Requisito funcional:</b> o que o sistema deve fazer','<b>Não funcional:</b> qualidade, desempenho, segurança, usabilidade etc.','<b>História de usuário:</b> Como [papel], quero [objetivo], para [valor]','<b>Critério de aceitação:</b> condição verificável para considerar algo pronto','<b>Caso de uso:</b> interação ator ↔ sistema para atingir um objetivo','<b>UML:</b> casos de uso, classes, sequência, atividade e estados','<b>Classe:</b> atributos + operações; associações modelam relações','<b>Validação:</b> confirmar se requisitos representam a necessidade real'],'tip':'Requisito bom deve ser claro, testável e sem ambiguidade. Se não dá para verificar depois, provavelmente ainda está vago.'},
{'title':'ARQUITETURA, DESIGN<br/>&amp; QUALIDADE','color':BERRY,'tint':BERRY_T,'kind':'arquitetura','idea':'Estruturar o sistema para reduzir acoplamento, aumentar coesão e facilitar evolução e manutenção.','formulas':['<b>Coesão:</b> responsabilidades relacionadas ficam juntas','<b>Acoplamento:</b> dependências entre módulos; quanto menor, melhor','<b>SOLID:</b> princípios para design orientado a objetos sustentável','<b>Camadas:</b> apresentação, negócio e dados separam responsabilidades','<b>MVC:</b> Model, View e Controller','<b>API:</b> contrato de comunicação entre componentes/sistemas','<b>Padrões:</b> soluções recorrentes como Factory, Strategy e Observer','<b>Qualidade:</b> manutenibilidade, confiabilidade, segurança e desempenho'],'tip':'Prefira módulos pequenos, coesos e com interfaces claras. Alta coesão + baixo acoplamento facilita teste, troca e evolução.'},
{'title':'TESTES, VERSIONAMENTO<br/>&amp; MANUTENÇÃO','color':GREEN,'tint':GREEN_T,'kind':'testes','idea':'Controlar mudanças e detectar defeitos cedo por automação, integração contínua e disciplina de manutenção.','formulas':['<b>Unitário:</b> verifica uma unidade isolada','<b>Integração:</b> verifica interação entre módulos','<b>Sistema:</b> valida o produto completo','<b>Regressão:</b> verifica se mudanças quebraram algo','<b>Pirâmide:</b> muitos unitários; poucos E2E','<b>Git:</b> commit, branch, merge e pull request','<b>CI/CD:</b> build, testes e entrega automatizados'],'tip':'Automatize o que é repetitivo. Testes e versionamento não eliminam defeitos, mas tornam mudanças mais seguras e rastreáveis.'}
]

CARD_TOP=PAGE_H-16; CARD_BOTTOM=16; CARD_H=CARD_TOP-CARD_BOTTOM; GAP=14; CARD_W=(PAGE_W-2*MARGIN-3*GAP)/4
STYLE_TITLE=ParagraphStyle('title',fontName='DVCond-Bold',fontSize=17.2,leading=18.6,textColor=WHITE,alignment=1)
STYLE_IDEA=ParagraphStyle('idea',fontName='DVCond-Oblique',fontSize=12.6,leading=15.6,textColor=MUTED)
STYLE_TIP=ParagraphStyle('tip',fontName='DVCond',fontSize=11.7,leading=14.7,textColor=INK)

def arrow(c,x1,y1,x2,y2,color,width=1.1,head=4):
    c.setStrokeColor(color); c.setFillColor(color); c.setLineWidth(width); c.line(x1,y1,x2,y2); a=math.atan2(y2-y1,x2-x1)
    for d in (2.55,-2.55): c.line(x2,y2,x2+head*math.cos(a+d),y2+head*math.sin(a+d))

def box(c,x,y,w,h,color,label):
    c.setStrokeColor(color); c.setFillColor(HexColor('#F8FAFD')); c.setLineWidth(1.1); c.roundRect(x,y,w,h,3,fill=1,stroke=1); c.setFillColor(INK); c.setFont('DVCond-Bold',8); c.drawCentredString(x+w/2,y+h/2-3,label)

def diagram_processos(c,ox,oy,dw,dh,color):
    labels=['Req.','Projeto','Código','Teste']
    xs=[ox+dw*.06,ox+dw*.29,ox+dw*.52,ox+dw*.75]; y=oy+dh*.48
    for x,l in zip(xs,labels): box(c,x,y,38,18,color,l)
    for i in range(3): arrow(c,xs[i]+38,y+9,xs[i+1]-4,y+9,color,1.0,3.5)
    c.setFillColor(MUTED); c.setFont('DVCond-Bold',8.8); c.drawCentredString(ox+dw*.5,oy+dh*.18,'iterar  •  entregar  •  aprender')

def diagram_requisitos(c,ox,oy,dw,dh,color):
    cx=ox+dw*.22; cy=oy+dh*.52
    c.setStrokeColor(color); c.setLineWidth(1.2); c.circle(cx,cy,9,stroke=1,fill=0); c.line(cx,cy-9,cx,cy-27); c.line(cx-10,cy-17,cx+10,cy-17); c.line(cx,cy-27,cx-8,cy-39); c.line(cx,cy-27,cx+8,cy-39)
    box(c,ox+dw*.48,oy+dh*.40,70,28,color,'SISTEMA')
    arrow(c,cx+12,cy-12,ox+dw*.48-4,oy+dh*.54,color,1.0,3.5)
    c.setFillColor(INK); c.setFont('DVCond-Bold',9); c.drawCentredString(ox+dw*.54,oy+dh*.18,'ator  →  caso de uso  →  regra')

def diagram_arquitetura(c,ox,oy,dw,dh,color):
    x=ox+dw*.20; y=oy+dh*.20; w=dw*.60; h=14
    for i,lab in enumerate(['UI','Negócio','Dados']): box(c,x,y+i*18,w,h,color,lab)
    c.setFillColor(MUTED); c.setFont('DVCond-Bold',8.2); c.drawCentredString(ox+dw*.5,oy+dh*.90,'camadas + interfaces')

def diagram_testes(c,ox,oy,dw,dh,color):
    # pyramid
    cx=ox+dw*.33; by=oy+dh*.20
    levels=[(56,'Unit.'),(40,'Integração'),(24,'E2E')]
    for i,(w,l) in enumerate(levels):
        y=by+i*16; x=cx-w/2; c.setStrokeColor(color); c.setLineWidth(1.1); c.rect(x,y,w,12,stroke=1,fill=0); c.setFillColor(INK); c.setFont('DVCond-Bold',7.2); c.drawCentredString(cx,y+3,l)
    box(c,ox+dw*.62,oy+dh*.43,46,18,color,'Git')
    box(c,ox+dw*.62,oy+dh*.20,46,18,color,'CI/CD')
    arrow(c,ox+dw*.62+23,oy+dh*.41,ox+dw*.62+23,oy+dh*.38,color,1.0,3.5)

DIAGRAMS={'processos':diagram_processos,'requisitos':diagram_requisitos,'arquitetura':diagram_arquitetura,'testes':diagram_testes}

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

c=canvas.Canvas(str(OUT),pagesize=landscape(A4)); c.setTitle('Engenharia de Software - Cheat Sheet OneNote'); c.setAuthor('OpenAI')
c.setFillColor(BG); c.rect(0,0,PAGE_W,PAGE_H,fill=1,stroke=0); c.setStrokeColor(GRID); c.setLineWidth(.35)
step=16; x=0
while x<PAGE_W: c.line(x,0,x,PAGE_H); x+=step
y=0
while y<PAGE_H: c.line(0,y,PAGE_W,y); y+=step
x=MARGIN
for card in CARDS: draw_card(c,card,x); x+=CARD_W+GAP
c.save(); print(OUT)
