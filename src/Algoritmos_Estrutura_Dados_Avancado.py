import math
from pathlib import Path
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph

OUT = Path('/mnt/data/Algoritmos_Estrutura_Dados_Avancado_OneNote.pdf')
PAGE_W, PAGE_H = landscape(A4); MARGIN = 16
FONT_DIR = Path('/usr/share/fonts/truetype/dejavu')
pdfmetrics.registerFont(TTFont('DVCond', str(FONT_DIR/'DejaVuSansCondensed.ttf')))
pdfmetrics.registerFont(TTFont('DVCond-Bold', str(FONT_DIR/'DejaVuSansCondensed-Bold.ttf')))
pdfmetrics.registerFont(TTFont('DVCond-Oblique', str(FONT_DIR/'DejaVuSansCondensed-Oblique.ttf')))
pdfmetrics.registerFontFamily('DVCond', normal='DVCond', bold='DVCond-Bold', italic='DVCond-Oblique', boldItalic='DVCond-Bold')

BG=HexColor('#F6F8FB'); GRID=HexColor('#E6EBF3'); INK=HexColor('#1C2B4A'); MUTED=HexColor('#5A6B8C'); WHITE=HexColor('#FFFFFF'); LINE=HexColor('#E7ECF4'); AXIS=HexColor('#D7DEEA')
TEAL,TEAL_T=HexColor('#147D82'),HexColor('#E3F2F1'); AMBER,AMBER_T=HexColor('#C97A1A'),HexColor('#FBEDDD'); BERRY,BERRY_T=HexColor('#A83E63'),HexColor('#F6E4EB'); GREEN,GREEN_T=HexColor('#2F7A4F'),HexColor('#E2F0E7')

CARDS=[
{'title':'ÁRVORES BALANCEADAS<br/>&amp; MULTIVIAS','color':TEAL,'tint':TEAL_T,'kind':'arvores','idea':'Manter operações eficientes controlando a altura e a organização das chaves na árvore.','formulas':['<b>AVL:</b> |altura(esq) − altura(dir)| ≤ 1','<b>Rotações:</b> simples ou duplas restauram o balanceamento','<b>Busca/ins./remoção:</b> O(log n) em árvore balanceada','<b>Red-Black:</b> balanceamento aproximado com regras de cores','<b>B-Tree:</b> vários filhos/chaves por nó; ideal para disco','<b>B+ Tree:</b> dados nas folhas; folhas encadeadas','<b>Trie:</b> busca por prefixos em O(m), m = tamanho da chave','<b>Uso:</b> índices, sistemas de arquivos e bancos de dados'],'tip':'Em estruturas balanceadas, o ganho vem de manter a altura próxima de log n. Uma BST comum pode degradar para O(n).'},
{'title':'GRAFOS &amp;<br/>ALGORITMOS CLÁSSICOS','color':AMBER,'tint':AMBER_T,'kind':'grafos','idea':'Resolver conectividade, caminhos mínimos e árvores geradoras em redes e relações complexas.','formulas':['<b>Representação:</b> lista de adjacência ou matriz','<b>BFS:</b> O(V+E); menor caminho em grafo não ponderado','<b>DFS:</b> O(V+E); ciclos, componentes e ordenação topológica','<b>Dijkstra:</b> caminhos mínimos com pesos não negativos','<b>Bellman-Ford:</b> aceita pesos negativos e detecta ciclos negativos','<b>Floyd-Warshall:</b> todos os pares em O(V³)','<b>Prim/Kruskal:</b> árvore geradora mínima (MST)','<b>Topológica:</b> ordena DAG respeitando dependências'],'tip':'Antes de escolher o algoritmo, observe se há pesos negativos, se o grafo é direcionado e se você precisa de um caminho ou de todos.'},
{'title':'HASHING &amp;<br/>ESTRUTURAS ESPECIAIS','color':BERRY,'tint':BERRY_T,'kind':'hash','idea':'Usar estruturas especializadas para consultas rápidas, conjuntos dinâmicos e processamento de intervalos.','formulas':['<b>Hashing:</b> custo médio O(1) para busca/inserção','<b>Fator de carga:</b> α = n/m; controla colisões','<b>Rehash:</b> aumenta tabela quando α fica alto','<b>Union-Find:</b> conjuntos disjuntos com find/union','<b>Path compression:</b> encurta caminhos no find','<b>Union by rank/size:</b> evita árvores altas','<b>Segment Tree:</b> consultas/atualizações em intervalos O(log n)','<b>Fenwick Tree:</b> somas prefixadas com O(log n) e pouca memória'],'tip':'Escolha pela operação dominante: hash para chave→valor, Union-Find para conectividade dinâmica e Segment/Fenwick para intervalos.'},
{'title':'DP, GREEDY &amp;<br/>BACKTRACKING','color':GREEN,'tint':GREEN_T,'kind':'estrategias','idea':'Escolher estratégias algorítmicas para reduzir recomputação e explorar espaços de busca com eficiência.','formulas':['<b>DP:</b> subproblemas sobrepostos + subestrutura ótima','<b>Memoization:</b> top-down com cache','<b>Tabulation:</b> bottom-up preenchendo tabela','<b>Greedy:</b> escolhe melhor decisão local a cada passo','<b>Backtracking:</b> tenta, valida e desfaz quando necessário','<b>Branch &amp; Bound:</b> poda ramos usando limites','<b>Amortizada:</b> custo médio de uma sequência de operações','<b>Trade-off:</b> tempo × memória × simplicidade da solução'],'tip':'DP não é “usar tabela” por si só. Primeiro identifique estados, transições, caso base e ordem correta de cálculo.'}
]

CARD_TOP=PAGE_H-16; CARD_BOTTOM=16; CARD_H=CARD_TOP-CARD_BOTTOM; GAP=14; CARD_W=(PAGE_W-2*MARGIN-3*GAP)/4
STYLE_TITLE=ParagraphStyle('card_title',fontName='DVCond-Bold',fontSize=17.2,leading=18.6,textColor=WHITE,alignment=1)
STYLE_IDEA=ParagraphStyle('idea',fontName='DVCond-Oblique',fontSize=12.6,leading=15.6,textColor=MUTED)
STYLE_TIP=ParagraphStyle('tip',fontName='DVCond',fontSize=11.7,leading=14.7,textColor=INK)

def arrow(c,x1,y1,x2,y2,color,width=1.1,head=4):
 c.setStrokeColor(color); c.setFillColor(color); c.setLineWidth(width); c.line(x1,y1,x2,y2); a=math.atan2(y2-y1,x2-x1)
 for d in (2.55,-2.55): c.line(x2,y2,x2+head*math.cos(a+d),y2+head*math.sin(a+d))

def node(c,x,y,color,label='',r=6):
 c.setStrokeColor(color); c.setFillColor(WHITE); c.setLineWidth(1.2); c.circle(x,y,r,stroke=1,fill=1)
 if label:
  c.setFillColor(INK); c.setFont('DVCond-Bold',6.8); c.drawCentredString(x,y-2.2,label)

def diagram_arvores(c,ox,oy,dw,dh,color):
 pts=[(ox+dw*.50,oy+dh*.68),(ox+dw*.28,oy+dh*.45),(ox+dw*.72,oy+dh*.45),(ox+dw*.18,oy+dh*.24),(ox+dw*.38,oy+dh*.24),(ox+dw*.62,oy+dh*.24),(ox+dw*.82,oy+dh*.24)]
 c.setStrokeColor(color); c.setLineWidth(1.1)
 for a,b in [(0,1),(0,2),(1,3),(1,4),(2,5),(2,6)]: c.line(*pts[a],*pts[b])
 for i,(x,y) in enumerate(pts): node(c,x,y,color,str([8,4,12,2,6,10,14][i]))
 c.setFillColor(INK); c.setFont('DVCond-Bold',9); c.drawCentredString(ox+dw*.50,oy+dh*.10,'altura ≈ log n')

def diagram_grafos(c,ox,oy,dw,dh,color):
 pts=[(ox+dw*.18,oy+dh*.58),(ox+dw*.42,oy+dh*.70),(ox+dw*.66,oy+dh*.58),(ox+dw*.30,oy+dh*.28),(ox+dw*.58,oy+dh*.28),(ox+dw*.82,oy+dh*.40)]
 edges=[(0,1),(1,2),(0,3),(1,4),(2,4),(2,5),(3,4),(4,5)]
 c.setStrokeColor(color); c.setLineWidth(1.1)
 for a,b in edges: c.line(*pts[a],*pts[b])
 for i,(x,y) in enumerate(pts): node(c,x,y,color,chr(65+i))
 c.setFillColor(INK); c.setFont('DVCond-Bold',8.8); c.drawCentredString(ox+dw*.50,oy+dh*.10,'BFS • DFS • menor caminho • MST')

def diagram_hash(c,ox,oy,dw,dh,color):
 # hash table
 x=ox+dw*.08; y=oy+dh*.20
 for i in range(4):
  c.setStrokeColor(color); c.rect(x,y+i*15,26,13,stroke=1,fill=0); c.setFillColor(INK); c.setFont('DVCond-Bold',7.3); c.drawCentredString(x+13,y+i*15+4,str(i))
 arrow(c,x+38,y+47,x+70,y+47,color,1,3.5); c.setFillColor(MUTED); c.setFont('DVCond-Bold',8); c.drawString(x+38,y+55,'h(k)')
 # union find tree
 cx=ox+dw*.70; cy=oy+dh*.62; pts=[(cx,cy),(cx-18,cy-18),(cx+18,cy-18),(cx-26,cy-36),(cx+26,cy-36)]
 c.setStrokeColor(color)
 for a,b in [(0,1),(0,2),(1,3),(2,4)]: c.line(*pts[a],*pts[b])
 for p in pts: node(c,*p,color,r=5)
 c.setFillColor(INK); c.setFont('DVCond-Bold',8.8); c.drawCentredString(ox+dw*.58,oy+dh*.10,'hash   •   union-find')

def diagram_estrategias(c,ox,oy,dw,dh,color):
 # DP table
 x=ox+dw*.08; y=oy+dh*.25; s=12
 for r in range(3):
  for cc in range(4): c.setStrokeColor(color); c.rect(x+cc*s,y+r*s,s,s,stroke=1,fill=0)
 # decision tree
 root=(ox+dw*.70,oy+dh*.68); a=(ox+dw*.58,oy+dh*.46); b=(ox+dw*.82,oy+dh*.46); c1=(ox+dw*.52,oy+dh*.27); c2=(ox+dw*.64,oy+dh*.27); c3=(ox+dw*.76,oy+dh*.27); c4=(ox+dw*.88,oy+dh*.27)
 c.setStrokeColor(color); c.setLineWidth(1.0)
 for u,v in [(root,a),(root,b),(a,c1),(a,c2),(b,c3),(b,c4)]: c.line(*u,*v)
 for p in [root,a,b,c1,c2,c3,c4]: node(c,*p,color,r=4.5)
 c.setFillColor(INK); c.setFont('DVCond-Bold',8.6); c.drawCentredString(ox+dw*.48,oy+dh*.10,'DP   •   greedy   •   backtracking')

DIAGRAMS={'arvores':diagram_arvores,'grafos':diagram_grafos,'hash':diagram_hash,'estrategias':diagram_estrategias}

def draw_card(c,card,cx):
 color,tint=card['color'],card['tint']; c.setFillColor(WHITE); c.setStrokeColor(color); c.setLineWidth(1.5); c.roundRect(cx,CARD_BOTTOM,CARD_W,CARD_H,10,fill=1,stroke=1)
 header_h=58; header_y=CARD_TOP-7-header_h; c.setFillColor(color); c.roundRect(cx+5,header_y,CARD_W-10,header_h,6,fill=1,stroke=0)
 p=Paragraph(card['title'],STYLE_TITLE); _,ph=p.wrapOn(c,CARD_W-22,header_h-6); p.drawOn(c,cx+11,header_y+(header_h-ph)/2)
 cursor=header_y-11; dh=76; dy=cursor-dh; DIAGRAMS[card['kind']](c,cx+11,dy,CARD_W-22,dh,color); cursor=dy-10
 p=Paragraph(card['idea'],STYLE_IDEA); _,ph=p.wrapOn(c,CARD_W-22,70); p.drawOn(c,cx+11,cursor-ph); cursor-=ph+9
 c.setStrokeColor(LINE); c.setLineWidth(.8); c.line(cx+11,cursor,cx+CARD_W-11,cursor); cursor-=10
 tip_y=CARD_BOTTOM+8; tip=Paragraph('<b>Dica:</b> '+card['tip'],STYLE_TIP); _,tip_txt_h=tip.wrapOn(c,CARD_W-34,130); tip_h=max(72,tip_txt_h+22); tip_top=tip_y+tip_h
 html='<br/>'.join('• '+x for x in card['formulas']); available=cursor-tip_top-10; fs=10.65; lead=13.55
 while True:
  st=ParagraphStyle('body_'+card['kind'],fontName='DVCond',fontSize=fs,leading=lead,textColor=INK); body=Paragraph(html,st); _,bh=body.wrapOn(c,CARD_W-22,470)
  if bh<=available or fs<=9.8: break
  fs-=.1; lead-=.1
 body.drawOn(c,cx+11,cursor-bh)
 c.setFillColor(tint); c.roundRect(cx+7,tip_y,CARD_W-14,tip_h,6,fill=1,stroke=0); tip.drawOn(c,cx+17,tip_y+(tip_h-tip_txt_h)/2)

c=canvas.Canvas(str(OUT),pagesize=landscape(A4)); c.setTitle('Algoritmos e Estrutura de Dados Avançado - Cheat Sheet OneNote'); c.setAuthor('OpenAI')
c.setFillColor(BG); c.rect(0,0,PAGE_W,PAGE_H,fill=1,stroke=0); c.setStrokeColor(GRID); c.setLineWidth(.35)
step=16; x=0
while x<PAGE_W: c.line(x,0,x,PAGE_H); x+=step
y=0
while y<PAGE_H: c.line(0,y,PAGE_W,y); y+=step
x=MARGIN
for card in CARDS: draw_card(c,card,x); x+=CARD_W+GAP
c.save(); print(OUT)
