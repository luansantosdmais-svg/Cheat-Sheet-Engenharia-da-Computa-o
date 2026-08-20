import math
from pathlib import Path
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph

OUT = Path('/mnt/data/Algoritmos_Logica_Programacao_OneNote.pdf')
PAGE_W, PAGE_H = landscape(A4)
MARGIN = 16
FONT_DIR = Path('/usr/share/fonts/truetype/dejavu')
pdfmetrics.registerFont(TTFont('DVCond', str(FONT_DIR / 'DejaVuSansCondensed.ttf')))
pdfmetrics.registerFont(TTFont('DVCond-Bold', str(FONT_DIR / 'DejaVuSansCondensed-Bold.ttf')))
pdfmetrics.registerFont(TTFont('DVCond-Oblique', str(FONT_DIR / 'DejaVuSansCondensed-Oblique.ttf')))
pdfmetrics.registerFontFamily('DVCond', normal='DVCond', bold='DVCond-Bold', italic='DVCond-Oblique', boldItalic='DVCond-Bold')

BG=HexColor('#F6F8FB'); GRID=HexColor('#E6EBF3'); INK=HexColor('#1C2B4A'); MUTED=HexColor('#5A6B8C'); WHITE=HexColor('#FFFFFF'); LINE=HexColor('#E7ECF4'); AXIS=HexColor('#D7DEEA')
TEAL,TEAL_T=HexColor('#147D82'),HexColor('#E3F2F1'); AMBER,AMBER_T=HexColor('#C97A1A'),HexColor('#FBEDDD'); BERRY,BERRY_T=HexColor('#A83E63'),HexColor('#F6E4EB'); GREEN,GREEN_T=HexColor('#2F7A4F'),HexColor('#E2F0E7')

CARDS=[
 {'title':'LÓGICA, VARIÁVEIS<br/>&amp; OPERADORES','color':TEAL,'tint':TEAL_T,'kind':'logica','idea':'Transformar um problema em passos claros usando dados, expressões e operadores.','formulas':[
  '<b>Algoritmo:</b> sequência finita e ordenada de passos',
  '<b>Variável:</b> nome que referencia um valor na memória',
  '<b>Tipos:</b> inteiro, real, lógico, caractere e texto',
  '<b>Atribuição:</b> x ← expressão',
  '<b>Aritméticos:</b> +, −, ×, ÷, mod',
  '<b>Relacionais:</b> =, ≠, &lt;, &gt;, ≤, ≥',
  '<b>Lógicos:</b> NÃO, E, OU',
  '<b>Prioridade:</b> parênteses → aritméticos → relacionais → lógicos',
 ],'tip':'Antes de programar, escreva entradas, processamento e saídas. Um algoritmo claro costuma virar código claro.'},
 {'title':'DECISÕES &amp;<br/>ESTRUTURAS DE CONTROLE','color':AMBER,'tint':AMBER_T,'kind':'decisao','idea':'Escolher caminhos diferentes conforme condições verdadeiras ou falsas.','formulas':[
  '<b>SE:</b> executa um bloco quando a condição é verdadeira',
  '<b>SE/SENÃO:</b> escolhe entre dois caminhos',
  '<b>Encadeado:</b> use quando há várias faixas ou condições',
  '<b>ESCOLHA/CASO:</b> útil para valores discretos de uma variável',
  '<b>Condição composta:</b> combine testes com E / OU',
  '<b>Curto-circuito:</b> a avaliação pode parar quando o resultado já é conhecido',
  '<b>Validação:</b> trate entradas inválidas explicitamente',
  '<b>Boa prática:</b> evite níveis excessivos de aninhamento',
 ],'tip':'Teste mentalmente os casos de fronteira: igual, menor, maior, zero, vazio e valores extremos. É onde muitos erros aparecem.'},
 {'title':'REPETIÇÃO &amp;<br/>RASTREAMENTO','color':BERRY,'tint':BERRY_T,'kind':'laco','idea':'Repetir instruções de forma controlada e acompanhar a evolução das variáveis.','formulas':[
  '<b>PARA:</b> ideal quando o número de repetições é conhecido',
  '<b>ENQUANTO:</b> testa a condição antes de executar',
  '<b>REPITA:</b> executa ao menos uma vez e testa no final',
  '<b>Contador:</b> i ← i + 1',
  '<b>Acumulador:</b> soma ← soma + valor',
  '<b>Sentinela:</b> valor especial encerra a leitura',
  '<b>Loop infinito:</b> condição nunca se torna falsa',
  '<b>Rastreamento:</b> monte tabela com iteração, variáveis e saída',
 ],'tip':'Em todo laço, identifique três coisas: inicialização, condição de parada e atualização. Se uma faltar, suspeite de erro.'},
 {'title':'FUNÇÕES &amp;<br/>MODULARIZAÇÃO','color':GREEN,'tint':GREEN_T,'kind':'modular','idea':'Dividir problemas em partes menores, reutilizáveis e fáceis de testar.','formulas':[
  '<b>Função:</b> recebe parâmetros e pode retornar um valor',
  '<b>Procedimento:</b> executa uma tarefa sem retorno obrigatório',
  '<b>Parâmetro:</b> dado enviado para a rotina',
  '<b>Escopo:</b> define onde uma variável pode ser acessada',
  '<b>Vetor:</b> coleção indexada de elementos do mesmo tipo',
  '<b>Índice:</b> posição usada para acessar vetor[i]',
  '<b>Matriz:</b> estrutura bidimensional linha × coluna',
  '<b>Modularização:</b> reduz repetição e facilita manutenção/testes',
 ],'tip':'Dê a cada função uma responsabilidade principal. Funções pequenas e bem nomeadas são mais fáceis de entender, testar e reutilizar.'}
]

CARD_TOP=PAGE_H-16; CARD_BOTTOM=16; CARD_H=CARD_TOP-CARD_BOTTOM; GAP=14; CARD_W=(PAGE_W-2*MARGIN-3*GAP)/4
STYLE_TITLE=ParagraphStyle('card_title',fontName='DVCond-Bold',fontSize=17.2,leading=18.6,textColor=WHITE,alignment=1,spaceAfter=0)
STYLE_IDEA=ParagraphStyle('idea',fontName='DVCond-Oblique',fontSize=12.6,leading=15.6,textColor=MUTED)
STYLE_TIP=ParagraphStyle('tip',fontName='DVCond',fontSize=11.7,leading=14.7,textColor=INK)

def arrow(c,x1,y1,x2,y2,color,width=1.2,head=5):
 c.setStrokeColor(color); c.setFillColor(color); c.setLineWidth(width); c.line(x1,y1,x2,y2); ang=math.atan2(y2-y1,x2-x1)
 for d in (2.55,-2.55): c.line(x2,y2,x2+head*math.cos(ang+d),y2+head*math.sin(ang+d))

def diagram_logica(c,ox,oy,dw,dh,color):
 y=oy+dh*0.55; xs=[ox+dw*0.12,ox+dw*0.40,ox+dw*0.68]
 labels=['Entrada','Processa','Saída']
 for x,l in zip(xs,labels):
  c.setFillColor(HexColor('#F8FAFD')); c.setStrokeColor(color); c.setLineWidth(1.3); c.roundRect(x,y-13,45,26,4,fill=1,stroke=1)
  c.setFillColor(INK); c.setFont('DVCond-Bold',8.7); c.drawCentredString(x+22.5,y-3,l)
 arrow(c,xs[0]+45,y,xs[1]-4,y,color,1.1,4); arrow(c,xs[1]+45,y,xs[2]-4,y,color,1.1,4)
 c.setFillColor(color); c.setFont('DVCond-Bold',10.2); c.drawCentredString(ox+dw/2,oy+dh*0.16,'dados  →  regras  →  resultado')

def diamond(c,cx,cy,w,h,color):
 c.setStrokeColor(color); c.setLineWidth(1.4); p=c.beginPath(); p.moveTo(cx,cy+h/2); p.lineTo(cx+w/2,cy); p.lineTo(cx,cy-h/2); p.lineTo(cx-w/2,cy); p.close(); c.drawPath(p,stroke=1,fill=0)

def diagram_decisao(c,ox,oy,dw,dh,color):
 cx=ox+dw*0.50; cy=oy+dh*0.58; diamond(c,cx,cy,58,34,color)
 c.setFillColor(INK); c.setFont('DVCond-Bold',9.2); c.drawCentredString(cx,cy-3,'condição?')
 arrow(c,cx-29,cy,cx-64,cy,color,1.0,4); arrow(c,cx+29,cy,cx+64,cy,color,1.0,4)
 c.setFillColor(color); c.setFont('DVCond-Bold',9.4); c.drawCentredString(cx-52,cy+9,'SIM'); c.drawCentredString(cx+52,cy+9,'NÃO')
 c.setFillColor(INK); c.setFont('DVCond-Bold',10.0); c.drawCentredString(cx,oy+dh*0.16,'SE  •  SENÃO  •  CASO')

def diagram_laco(c,ox,oy,dw,dh,color):
 cx=ox+dw*0.50; cy=oy+dh*0.54
 c.setStrokeColor(color); c.setLineWidth(1.5); c.circle(cx,cy,27,stroke=1,fill=0)
 arrow(c,cx+12,cy+24,cx+27,cy+5,color,1.1,4)
 arrow(c,cx-12,cy-24,cx-27,cy-5,color,1.1,4)
 c.setFillColor(INK); c.setFont('DVCond-Bold',10.5); c.drawCentredString(cx,cy+2,'repete'); c.drawCentredString(cx,cy-11,'até parar')
 c.setFillColor(color); c.setFont('DVCond-Bold',10.0); c.drawCentredString(cx,oy+dh*0.14,'inicializa  →  testa  →  atualiza')

def diagram_modular(c,ox,oy,dw,dh,color):
 cx=ox+dw*0.50; top=oy+dh*0.78
 c.setFillColor(HexColor('#F8FAFD')); c.setStrokeColor(color); c.setLineWidth(1.3); c.roundRect(cx-35,top-13,70,26,4,fill=1,stroke=1)
 c.setFillColor(INK); c.setFont('DVCond-Bold',9.2); c.drawCentredString(cx,top-3,'programa')
 children=[cx-dw*0.26,cx,cx+dw*0.26]
 for i,x in enumerate(children,1):
  arrow(c,cx,top-13,x,oy+dh*0.48+13,color,0.9,3.5)
  c.setFillColor(HexColor('#F8FAFD')); c.setStrokeColor(color); c.roundRect(x-27,oy+dh*0.48-13,54,26,4,fill=1,stroke=1)
  c.setFillColor(INK); c.setFont('DVCond-Bold',8.7); c.drawCentredString(x,oy+dh*0.48-3,f'função {i}')
 c.setFillColor(color); c.setFont('DVCond-Bold',10.0); c.drawCentredString(cx,oy+dh*0.14,'dividir  •  testar  •  reutilizar')

DIAGRAMS={'logica':diagram_logica,'decisao':diagram_decisao,'laco':diagram_laco,'modular':diagram_modular}

def draw_card(c,card,cx):
 color,tint=card['color'],card['tint']; c.setFillColor(WHITE); c.setStrokeColor(color); c.setLineWidth(1.5); c.roundRect(cx,CARD_BOTTOM,CARD_W,CARD_H,10,fill=1,stroke=1)
 header_h=58; header_y=CARD_TOP-7-header_h; c.setFillColor(color); c.roundRect(cx+5,header_y,CARD_W-10,header_h,6,fill=1,stroke=0)
 title=Paragraph(card['title'],STYLE_TITLE); _,th=title.wrapOn(c,CARD_W-22,header_h-6); title.drawOn(c,cx+11,header_y+(header_h-th)/2)
 cursor=header_y-11; diagram_h=76; diagram_y=cursor-diagram_h; DIAGRAMS[card['kind']](c,cx+11,diagram_y,CARD_W-22,diagram_h,color); cursor=diagram_y-10
 idea=Paragraph(card['idea'],STYLE_IDEA); _,ih=idea.wrapOn(c,CARD_W-22,70); idea.drawOn(c,cx+11,cursor-ih); cursor-=ih+9
 c.setStrokeColor(LINE); c.setLineWidth(0.8); c.line(cx+11,cursor,cx+CARD_W-11,cursor); cursor-=10
 tip_y=CARD_BOTTOM+8; tip=Paragraph('<b>Dica:</b> '+card['tip'],STYLE_TIP); _,tth=tip.wrapOn(c,CARD_W-34,130); tip_h=max(72,tth+22); tip_top=tip_y+tip_h
 formula_html='<br/>'.join('• '+item for item in card['formulas']); available_h=cursor-tip_top-10; fs=11.15; leading=14.15
 while True:
  st=ParagraphStyle('formula_'+card['kind'],fontName='DVCond',fontSize=fs,leading=leading,textColor=INK); formulas=Paragraph(formula_html,st); _,fh=formulas.wrapOn(c,CARD_W-22,470)
  if fh<=available_h or fs<=10.2: break
  fs-=0.1; leading-=0.1
 formulas.drawOn(c,cx+11,cursor-fh)
 c.setFillColor(tint); c.roundRect(cx+7,tip_y,CARD_W-14,tip_h,6,fill=1,stroke=0); tip.drawOn(c,cx+17,tip_y+(tip_h-tth)/2)

c=canvas.Canvas(str(OUT),pagesize=landscape(A4)); c.setTitle('Algoritmos e Lógica de Programação - Cheat Sheet OneNote'); c.setAuthor('OpenAI')
c.setFillColor(BG); c.rect(0,0,PAGE_W,PAGE_H,fill=1,stroke=0); c.setStrokeColor(GRID); c.setLineWidth(0.35)
step=16; x=0
while x<PAGE_W: c.line(x,0,x,PAGE_H); x+=step
y=0
while y<PAGE_H: c.line(0,y,PAGE_W,y); y+=step
x=MARGIN
for card in CARDS: draw_card(c,card,x); x+=CARD_W+GAP
c.save(); print(f'PDF gerado em {OUT}')
