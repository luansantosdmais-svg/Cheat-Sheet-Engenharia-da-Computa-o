# -*- coding: utf-8 -*-
"""PARTE 2C: Programacao (Computacao Grafica, IA, Design Thinking)."""

SUBJECTS_2C = [
dict(
    stem="Computacao_Grafica_Processamento_Imagens", name="Computação Gráfica e Processamento de Imagens",
    cat="Programação", folder="03_Programacao", emoji="\U0001F3A8",
    tagline="Imagem digital, transformações geométricas, render e filtros.",
    about="Do pixel ao filtro: representação de imagens, transformações geométricas com matrizes "
          "homogêneas, convolução (blur/sobel) e histograma — tudo com NumPy.",
    examples=r'''
%matplotlib inline
import numpy as np
import matplotlib.pyplot as plt

print("=" * 60)
print("1) IMAGEM DIGITAL: matriz 4x4 em tons de cinza")
img = np.array([[0, 60, 120, 180],
                [60, 120, 180, 240],
                [120, 180, 240, 255],
                [180, 240, 255, 255]], dtype=np.uint8)
print(img)

print("\n2) TRANSFORMACAO 2D: rotacao de 30 graus (matriz homogenea)")
theta = np.radians(30)
R = np.array([[np.cos(theta), -np.sin(theta), 0],
              [np.sin(theta),  np.cos(theta), 0],
              [0, 0, 1]])
p = np.array([1, 0, 1])   # ponto (1,0) homogeneo
print("   R(30) * (1,0) =", (R @ p)[:2].round(3))
print("   (a ordem das transformacoes importa: R*T != T*R)")

print("\n3) CONVOLUCAO - filtro de suavizacao (media 3x3)")
im = np.zeros((50, 50)); im[20:30, 20:30] = 255
kernel = np.ones((3, 3))/9
def conv2d(a, k):
    out = np.zeros_like(a)
    p = k.shape[0]//2
    for i in range(p, a.shape[0]-p):
        for j in range(p, a.shape[1]-p):
            out[i, j] = (a[i-p:i+p+1, j-p:j+p+1]*k).sum()
    return out
suave = conv2d(im, kernel)

fig, ax = plt.subplots(1, 3, figsize=(9.5, 3.2))
ax[0].imshow(im, cmap="gray"); ax[0].set_title("original (quadrado)")
ax[1].imshow(suave, cmap="gray"); ax[1].set_title("suavizada (media 3x3)")
ax[2].hist(im.ravel(), bins=20, color="#147D82", alpha=.8)
ax[2].set_title("histograma da original")
for a in ax: a.grid(alpha=.2)
plt.tight_layout(); plt.show()

print("\n4) DETECCAO DE BORDAS - Sobel")
gx = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
gy = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])
fx = conv2d(im, gx); fy = conv2d(im, gy)
borda = np.sqrt(fx**2 + fy**2)
plt.figure(figsize=(6, 3))
plt.imshow(borda, cmap="gray"); plt.title("bordas detectadas (Sobel)")
plt.grid(alpha=.2); plt.tight_layout(); plt.show()

print("\n5) LIMIARIZACAO (segmentacao simples)")
limiar = 127
mask = (im > limiar).astype(int)
print(f"   pixels acima de {limiar}: {mask.sum()} (regiao do quadrado)")

print("\n6) TRANSFORMACAO DE INTENSIDADE (negativo e equalizacao simples)")
neg = 255 - im
eq = np.interp(im, (im.min(), im.max()), (0, 255)).astype(np.uint8)
fig2, ax2 = plt.subplots(1, 2, figsize=(6.5, 3))
ax2[0].imshow(neg, cmap="gray"); ax2[0].set_title("negativo")
ax2[1].imshow(eq, cmap="gray"); ax2[1].set_title("equalizado (estira contraste)")
plt.tight_layout(); plt.show()
print("\nOK - graficos e processamento de imagem com NumPy.")
'''),
dict(
    stem="Fundamentos_Inteligencia_Artificial", name="Fundamentos de Inteligência Artificial",
    cat="Programação", folder="03_Programacao", emoji="\U0001F916",
    tagline="Agentes, busca, lógica, aprendizado de máquina e redes neurais.",
    about="Fundamentos de IA: busca em grafos (BFS/DFS/A*), perceptron, regressão linear e "
          "kNN implementados do zero com NumPy.",
    examples=r'''
%matplotlib inline
import numpy as np
import matplotlib.pyplot as plt
from collections import deque

print("=" * 60)
print("1) BUSCA EM GRAFO - BFS e DFS")
grafo = {"A": ["B", "C"], "B": ["D", "E"], "C": ["F"], "D": [], "E": ["F"], "F": []}
def busca(g, inicio, alvo, modo="bfs"):
    fila = deque([inicio]); vis = {inicio}; pai = {inicio: None}
    while fila:
        v = fila.popleft() if modo == "bfs" else fila.pop()
        if v == alvo: break
        for nb in g[v]:
            if nb not in vis:
                vis.add(nb); pai[nb] = v
                fila.append(nb) if modo == "bfs" else fila.append(nb)
    caminho = []
    if alvo in pai:
        x = alvo
        while x is not None:
            caminho.append(x); x = pai[x]
        caminho.reverse()
    return caminho
print(f"   BFS A->F: {busca(grafo, 'A', 'F', 'bfs')}")
print(f"   DFS A->F: {busca(grafo, 'A', 'F', 'dfs')}")

print("\n2) PERCEPTRON: porta AND")
X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]], dtype=float)
y = np.array([0, 0, 0, 1])
w = np.zeros(2); b = 0.0; taxa = 0.1
for epoca in range(50):
    for xi, yi in zip(X, y):
        saida = 1 if (xi@w + b) >= 0 else 0
        erro = yi - saida
        w += taxa*erro*xi; b += taxa*erro
testes = [(xi, 1 if (xi@w + b) >= 0 else 0) for xi in X]
print(f"   pesos: {w.round(2)} | bias: {b:.2f} | previsoes: {[t[1] for t in testes]}")

print("\n3) REGRESSAO LINEAR (gradiente descendente)")
x = np.linspace(0, 10, 100)
y_real = 2.5*x + 3 + np.random.default_rng(0).normal(0, 1, 100)
a, b2, lr = 0.0, 0.0, 0.01
for _ in range(2000):
    pred = a*x + b2
    da = (2/len(x))*(x*(pred - y_real)).sum()
    db = (2/len(x))*(pred - y_real).sum()
    a -= lr*da; b2 -= lr*db
print(f"   modelo ajustado: y = {a:.2f}x + {b2:.2f} (real: y = 2.50x + 3.00)")

xx = np.linspace(0, 10, 20)
plt.figure(figsize=(6, 3.8))
plt.scatter(x, y_real, s=8, color="#888", label="dados")
plt.plot(xx, a*xx + b2, color="#147D82", lw=2, label="regressao")
plt.title("Regressao linear por gradiente descendente")
plt.legend(); plt.grid(alpha=.3); plt.tight_layout(); plt.show()

print("\n4) kNN (k vizinhos mais proximos) - classificacao")
from collections import Counter
dados = np.array([[1,1],[1,2],[2,2],[5,5],[6,5],[6,6]])
rotulos = np.array([0,0,0,1,1,1])
def knn(ponto, k=3):
    dist = np.sqrt(((dados - ponto)**2).sum(axis=1))
    viz = rotulos[np.argsort(dist)[:k]]
    return Counter(viz).most_common(1)[0][0]
for p in ([2,1], [5,6], [3,3]):
    print(f"   ponto {p} -> classe {knn(np.array(p, float))}")
print("\nOK - IA classica implementada do zero.")
'''),
dict(
    stem="Design_Thinking_Inovacao_Modelos_Negocios",
    name="Design Thinking, Inovação e Modelos de Negócios",
    cat="Programação", folder="03_Programacao", emoji="\U0001F4A1",
    tagline="Empatia, ideação, prototipação, Business Model Canvas e validação.",
    about="Inovação e modelos de negócio: Canvas estruturado, personas, análise SWOT, "
          "métricas de validação e projeção financeira simples.",
    examples=r'''
print("=" * 60)
print("1) BUSINESS MODEL CANVAS (estrutura em dados)")
canvas = {
    "Segmentos": ["Estudantes", "Profissionais"],
    "Proposta de Valor": ["Resumo rapido de materias", "Pratico e visual"],
    "Canais": ["GitHub", "YouTube"],
    "Relacionamento": ["Comunidade", "Feedback"],
    "Receitas": ["Gratuito + premium"],
    "Recursos": ["Conteudo", "Tempo"],
    "Atividades": ["Produzir", "Atualizar"],
    "Parcerias": ["Professores", "Faculdade"],
    "Custos": ["Hospedagem", "Ferramentas"],
}
for k, v in canvas.items():
    print(f"   {k:<20}: {', '.join(v)}")

print("\n2) PERSONA (exemplo sintetico)")
persona = {"Nome": "Carlos, 22", "Perfil": "Estudante de Eng. da Computacao",
           "Dores": ["Muita teoria espalhada", "Provas proximas"],
           "Necessidades": ["Resumo objetivo", "Exemplos praticos"]}
for k, v in persona.items():
    print(f"   {k:<12}: {v if isinstance(v, str) else ', '.join(v)}")

print("\n3) ANALISE SWOT")
swot = {"Forcas": ["Conteudo organizado", "Codigo executavel"],
        "Fraquezas": ["Pouca visibilidade"],
        "Oportunidades": ["SEO", "Parcerias"],
        "Ameacas": ["Muitos repositorios semelhantes"]}
for k, v in swot.items():
    print(f"   {k:<15}: {', '.join(v)}")

print("\n4) METRICAS DE VALIDACAO (MVP)")
metrica = {"visitas": 1200, "conversao": 0.045, "usuarios_ativos": 40}
metrica["clientes_potenciais"] = metrica["visitas"]*metrica["conversao"]
for k, v in metrica.items():
    print(f"   {k:<20}: {v}")

print("\n5) PROJECAO FINANCEIRA SIMPLES (5 meses)")
custo_mensal = 50
receita_mensal = 0
tabela = []
for mes in range(1, 6):
    receita_mensal += 120       # crescendo
    tabela.append((mes, custo_mensal, receita_mensal, receita_mensal - custo_mensal))
print("   mes | custo | receita | saldo")
for linha in tabela:
    print(f"   {linha[0]:>3} | {linha[1]:>5} | {linha[2]:>7} | {linha[3]:>6}")

print("\n6) CANVAS DE PROPOSTA DE VALOR")
proposta = {"Tarefas do cliente": ["Estudar", "Revisar"],
            "Dores": ["Ansiedade", "Falta de tempo"],
            "Ganhos": ["Confianca", "Aprovacao"],
            "Aliviadores": ["Resumos", "Checklists"],
            "Criadores de ganho": ["Exemplos reais", "Exercicios"]}
for k, v in proposta.items():
    print(f"   {k:<22}: {', '.join(v)}")
print("\nOK - inovacao e modelo de negocios estruturados.")
'''),
]