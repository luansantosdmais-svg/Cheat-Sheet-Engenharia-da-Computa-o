# -*- coding: utf-8 -*-
"""PARTE 2A: Programacao (3 primeiras materias)."""

SUBJECTS_2A = [
dict(
    stem="Algoritmos_Logica_Programacao", name="Algoritmos e Lógica de Programação",
    cat="Programação", folder="03_Programacao", emoji="\U0001F9E9",
    tagline="Algoritmos, variáveis, operadores, controle, laços, funções e modularização.",
    about="Base de tudo: como transformar problemas em passos lógicos. Exemplos de laços, "
          "condições, funções e algoritmos clássicos de busca e ordenação.",
    examples=r'''
import random

print("=" * 60)
print("1) ALGORITMO: numero primo? (otimizado)")
def primo(n):
    if n < 2: return False
    i = 2
    while i*i <= n:
        if n % i == 0: return False
        i += 1
    return True
for n in (2, 3, 17, 21, 97, 100):
    print(f"   {n:>3} -> primo: {primo(n)}")

print("\n2) LACO + ACUMULADOR: soma 1..100")
soma = 0
for i in range(1, 101):
    soma += i
print(f"   soma = {soma}")

print("\n3) DECISAO: classificar nota")
for nota in (3.5, 6.0, 8.5):
    st = "Aprovado" if nota >= 7 else ("Recuperacao" if nota >= 5 else "Reprovado")
    print(f"   nota {nota} -> {st}")

print("\n4) FIBONACCI (iterativo e recursivo)")
def fib_it(n):
    a, b = 0, 1
    for _ in range(n): a, b = b, a + b
    return a
def fib_rec(n):
    return n if n < 2 else fib_rec(n-1) + fib_rec(n-2)
print(f"   fib(10) iterativo = {fib_it(10)} | recursivo = {fib_rec(10)}")

print("\n5) FUNCAO + LISTA: media e desvio padrao")
def estatisticas(v):
    m = sum(v)/len(v)
    dp = (sum((x - m)**2 for x in v)/len(v))**0.5
    return m, dp
random.seed(1)
dados = [random.randint(1, 60) for _ in range(50)]
m, dp = estatisticas(dados)
print(f"   media = {m:.2f} | desvio = {dp:.2f} | menor = {min(dados)} | maior = {max(dados)}")

print("\n6) RASTREAMENTO: bubble sort passo a passo")
arr = [5, 3, 8, 1, 9, 2]
for passo in range(len(arr)-1):
    trocou = False
    for j in range(len(arr)-1-passo):
        if arr[j] > arr[j+1]:
            arr[j], arr[j+1] = arr[j+1], arr[j]
            trocou = True
    print(f"   passo {passo+1}: {arr}  {'(trocou)' if trocou else '(parou)'}")
    if not trocou: break
print("\nOK - logica de programacao demonstrada.")
'''),
dict(
    stem="Algoritmos_Estrutura_Dados", name="Algoritmos e Estruturas de Dados",
    cat="Programação", folder="03_Programacao", emoji="\U0001F4DA",
    tagline="Pilhas, filas, listas, árvores, busca, ordenação e complexidade.",
    about="Estruturas de dados clássicas e análise de complexidade: pilha, fila, lista ligada, "
          "árvore binária, busca binária e comparação de algoritmos de ordenação.",
    examples=r'''
import time
import random
from collections import deque

print("=" * 60)
print("1) PILHA (LIFO) e FILA (FIFO)")
pilha, fila = [], deque()
for x in "ABCD":
    pilha.append(x); fila.append(x)
print(f"   pilha: {[pilha.pop() for _ in range(len(pilha))]} (ultimo a entrar, primeiro a sair)")
print(f"   fila : {[fila.popleft() for _ in range(len(fila))]} (primeiro a entrar, primeiro a sair)")

print("\n2) LISTA LIGADA simples")
class No:
    def __init__(self, val): self.val, self.prox = val, None
class ListaLigada:
    def __init__(self): self.head = None
    def inserir(self, v):
        no = No(v); no.prox = self.head; self.head = no
    def percorrer(self):
        r, at = [], self.head
        while at: r.append(at.val); at = at.prox
        return r
    def buscar(self, v):
        at, pos = self.head, 0
        while at:
            if at.val == v: return pos
            at, pos = at.prox, pos + 1
        return -1
ll = ListaLigada()
for x in (3, 7, 1, 9): ll.inserir(x)
print(f"   lista: {ll.percorrer()} | buscar(7) na posicao {ll.buscar(7)}")

print("\n3) ARVORE BINARIA - percurso em ordem")
class NoArv:
    def __init__(self, v): self.v, self.e, self.d = v, None, None
def insere(no, v):
    if no is None: return NoArv(v)
    if v < no.v: no.e = insere(no.e, v)
    else: no.d = insere(no.d, v)
    return no
def em_ordem(no, out):
    if no: em_ordem(no.e, out); out.append(no.v); em_ordem(no.d, out)
raiz = None
for v in (50, 30, 70, 20, 40, 60, 80): raiz = insere(raiz, v)
o = []; em_ordem(raiz, o)
print(f"   em-ordem (sai ordenado): {o}")

print("\n4) BUSCA BINARIA em vetor ordenado (O(log n))")
vet = sorted(random.sample(range(1, 1000), 200))
def busca_binaria(v, alvo):
    lo, hi = 0, len(v) - 1
    passos = 0
    while lo <= hi:
        passos += 1
        mid = (lo + hi)//2
        if v[mid] == alvo: return mid, passos
        if v[mid] < alvo: lo = mid + 1
        else: hi = mid - 1
    return -1, passos
alvo = vet[57]
pos, passos = busca_binaria(vet, alvo)
print(f"   vetor com {len(vet)} itens -> encontrou {alvo} na pos {pos} em {passos} passos")

print("\n5) COMPLEXIDADE: ordenacao O(n^2) vs O(n log n)")
def bubble_sort(a):
    for i in range(len(a)):
        for j in range(len(a)-1-i):
            if a[j] > a[j+1]: a[j], a[j+1] = a[j+1], a[j]
    return a
random.seed(2)
tam = 3000
arr1 = [random.random() for _ in range(tam)]
arr2 = arr1[:]
t0 = time.perf_counter(); bubble_sort(arr1); t1 = time.perf_counter()
arr2.sort(); t2 = time.perf_counter()
print(f"   bubble sort (O(n^2)): {(t1-t0)*1000:.1f} ms")
print(f"   timsort    (O(nlogn)): {(t2-t1)*1000:.2f} ms")
print("\nOK - estruturas e complexidade demonstradas.")
'''),
dict(
    stem="Algoritmos_Estrutura_Dados_Avancado", name="Algoritmos e Estruturas de Dados Avançado",
    cat="Programação", folder="03_Programacao", emoji="\U0001F9E0",
    tagline="Árvores balanceadas, grafos, hashing, DP, greedy e backtracking.",
    about="Tópicos avançados: árvores AVL, grafos com Dijkstra, Union-Find, programação "
          "dinâmica e greedy aplicados a problemas clássicos.",
    examples=r'''
import heapq
from collections import deque

print("=" * 60)
print("1) GRAFO - BFS (largura) e DFS (profundidade)")
grafo = {"A": ["B", "C"], "B": ["A", "D", "E"], "C": ["A", "F"],
         "D": ["B"], "E": ["B", "F"], "F": ["C", "E"]}
def bfs(g, inicio):
    vis, fila = [inicio], deque([inicio])
    while fila:
        v = fila.popleft()
        for nb in g[v]:
            if nb not in vis:
                vis.append(nb); fila.append(nb)
    return vis
def dfs(g, inicio):
    vis, pilha = [], [inicio]
    while pilha:
        v = pilha.pop()
        if v not in vis:
            vis.append(v); pilha.extend(nb for nb in g[v] if nb not in vis)
    return vis
print(f"   BFS: {bfs(grafo, 'A')}")
print(f"   DFS: {dfs(grafo, 'A')}")

print("\n2) DIJKSTRA: menor caminho (custo) no grafo ponderado")
g = {"A": [("B", 4), ("C", 2)], "B": [("C", 1), ("D", 5)],
     "C": [("D", 8), ("E", 10)], "D": [("E", 2)], "E": []}
def dijkstra(g, inicio):
    dist = {v: float("inf") for v in g}
    dist[inicio] = 0
    pq = [(0, inicio)]
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]: continue
        for v, w in g[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(pq, (nd, v))
    return dist
d = dijkstra(g, "A")
print(f"   distancias de A: {d}")

print("\n3) UNION-FIND (conjuntos disjuntos)")
pai = {}
def find(x):
    if pai[x] != x: pai[x] = find(pai[x])
    return pai[x]
def union(a, b):
    ra, rb = find(a), find(b)
    if ra != rb: pai[rb] = ra
for x in "ABCDEFG": pai[x] = x
union("A", "B"); union("B", "C"); union("D", "E")
print(f"   A e C conectados? {find('A') == find('C')} | D e F? {find('D') == find('F')}")

print("\n4) PROGRAMACAO DINAMICA: mochila 0/1")
itens = [(60, 10), (100, 20), (120, 30)]  # (valor, peso)
capacidade = 50
dp = [[0]*(capacidade + 1) for _ in range(len(itens) + 1)]
for i in range(1, len(itens) + 1):
    v, p = itens[i-1]
    for c in range(capacidade + 1):
        dp[i][c] = dp[i-1][c]
        if p <= c:
            dp[i][c] = max(dp[i][c], dp[i-1][c - p] + v)
print(f"   valor maximo na mochila = {dp[-1][-1]}")

print("\n5) GREEDY: troco minimo com moedas")
moedas = [100, 50, 25, 10, 5, 1]
def troco(valor):
    usadas = []
    for m in moedas:
        while valor >= m:
            valor -= m; usadas.append(m)
    return usadas
print(f"   troco de 289: {troco(289)}")

print("\n6) HEAP: fila de prioridade")
h = []
for x in (7, 2, 9, 1, 5):
    heapq.heappush(h, x)
print(f"   removendo em ordem: {[heapq.heappop(h) for _ in range(len(h))]}")
print("\nOK - algoritmos avancados demonstrados.")
'''),
]