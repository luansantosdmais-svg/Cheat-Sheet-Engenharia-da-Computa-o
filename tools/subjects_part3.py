# -*- coding: utf-8 -*-
"""PARTE 3: Sistemas/Redes e Banco de Dados."""

SUBJECTS_3 = [
dict(
    stem="Sistemas_Operacionais", name="Sistemas Operacionais",
    cat="Sistemas/Redes", folder="04_Sistemas_e_Redes", emoji="\u2699\uFE0F",
    src="Sistemas_Operacionais_", cards_key="Sistemas_Operacionais_",
    tagline="Processos, threads, escalonamento, sincronização, memória e arquivos.",
    about="Núcleo do sistema operacional: escalonamento (FCFS/SJF/RR), sincronização com locks, "
          "substituição de páginas (FIFO/LRU) e concorrência — simulados em Python.",
    examples=r'''
%matplotlib inline
import threading
import numpy as np
import matplotlib.pyplot as plt

print("=" * 60)
print("1) ESCALONAMENTO - FCFS, SJF e Round Robin")
processos = [(1, 6), (2, 8), (3, 7), (4, 3)]  # (id, duracao)
def fcfs(p):
    t, saida = 0, []
    for pid, d in sorted(p):
        saida.append((pid, t, t + d)); t += d
    return saida
def sjf(p):
    t, saida, resto = 0, [], sorted(p, key=lambda x: x[1])
    for pid, d in resto:
        saida.append((pid, t, t + d)); t += d
    return saida
def rr(p, quantum=2):
    fila = list(p); t, saida, resto = 0, [], {}
    while fila:
        pid, d = fila.pop(0)
        executa = min(d, quantum)
        inicio = t; t += executa
        d -= executa
        if d > 0: fila.append((pid, d))
        else: saida.append((pid, inicio, t))
    return saida

def tempo_medio(saida):
    return sum(fim - t0 for _, t0, fim in saida)/len(saida)

for nome, fun in (("FCFS", fcfs), ("SJF", sjf), ("RR(q=2)", rr)):
    s = fun(processos)
    print(f"   {nome:<8} -> turnarround medio = {tempo_medio(s):.2f}  | {s}")

print("\n2) DIAGRAMA DE GANTT - Round Robin")
gantt = rr(processos)
fig, ax = plt.subplots(figsize=(7.5, 2.6))
cores = ["#147D82", "#C97A1A", "#A83E63", "#2F7A4F"]
for pid, t0, t1 in gantt:
    ax.barh(0, t1 - t0, left=t0, height=0.5, color=cores[pid-1], edgecolor="white")
    ax.text((t0 + t1)/2, 0, f"P{pid}", ha="center", va="center", color="white", fontweight="bold")
ax.set_yticks([]); ax.set_xlabel("tempo (u.t.)")
ax.set_title("Escalonamento Round Robin (quantum = 2)")
plt.tight_layout(); plt.show()

print("\n3) SINCRONIZACAO: incremento sem e com lock")
cont = [0]
def sem_lock(n=200000):
    for _ in range(n): cont[0] += 1
def com_lock(lk, n=200000):
    for _ in range(n):
        with lk: cont[0] += 1
ths = [threading.Thread(target=sem_lock) for _ in range(8)]
for t in ths: t.start()
for t in ths: t.join()
print(f"   sem lock: esperado 1600000, obtido {cont[0]}  -> RACE CONDITION")

cont[0] = 0
lk = threading.Lock()
ths = [threading.Thread(target=com_lock, args=(lk,)) for _ in range(8)]
for t in ths: t.start()
for t in ths: t.join()
print(f"   com lock: esperado 1600000, obtido {cont[0]}  -> OK")

print("\n4) MEMORIA VIRTUAL - substituicao de paginas FIFO vs LRU")
refs = [7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2, 1, 2, 0, 1, 7]
def fifo(refs, frames=3):
    mem, faltas = [], 0
    for r in refs:
        if r not in mem:
            faltas += 1
            if len(mem) == frames: mem.pop(0)
            mem.append(r)
    return faltas
def lru(refs, frames=3):
    mem, faltas = [], 0
    for r in refs:
        if r in mem:
            mem.remove(r); mem.append(r)
        else:
            faltas += 1
            if len(mem) == frames: mem.pop(0)
            mem.append(r)
    return faltas
print(f"   FIFO: {fifo(refs)} page faults | LRU: {lru(refs)} page faults "
      f"(3 molduras, sequencia de referencia classica)")

print("\n5) PROCESSO vs THREAD")
print("   Processo: espaco de endereco proprio, isolado, custo maior de criacao.")
print("   Thread:   compartilha memoria do processo, leve, precisa de sincronizacao.")

print("\n6) DEADLOCK: espera circular")
print("   P1 segura A e quer B | P2 segura B e quer A  -> deadlock (evite com ordem global)")

print("\nOK - sistema operacional simulado em Python.")
'''),
dict(
    stem="Redes_de_Computadores", name="Redes de Computadores",
    cat="Sistemas/Redes", folder="04_Sistemas_e_Redes", emoji="\U0001F310",
    tagline="Camadas, encapsulamento, IP, sub-redes, roteamento, TCP/UDP e segurança.",
    about="Redes de computadores na prática: endereçamento IP, cálculo de sub-redes CIDR, "
          "checksum, modelos de camadas e comparação TCP/UDP.",
    examples=r'''
import ipaddress

print("=" * 60)
print("1) ENDERECAMENTO IP: converter 192.168.1.10 para binario")
ip = ipaddress.ip_address("192.168.1.10")
print(f"   {ip} = {' . '.join(f'{int(o):08b}' for o in str(ip).split('.'))}")

print("\n2) SUBNETING (CIDR): rede 192.168.1.0/24")
rede = ipaddress.ip_network("192.168.1.0/24")
print(f"   rede: {rede} | broadcast: {rede.broadcast_address} | hosts: {rede.num_addresses - 2}")

print("\n3) DIVIDIR EM 4 SUB-REDES (2 bits de host)")
sub = list(rede.subnets(prefixlen_diff=2))
for s in sub:
    print(f"   {s} | broadcast {s.broadcast_address} | hosts {s.num_addresses - 2}")

print("\n4) CALCULO DE MASCARA: /26")
r26 = ipaddress.ip_network("10.0.0.0/26")
print(f"   mascara: {r26.netmask} | hosts uteis: {r26.num_addresses - 2}")

print("\n5) MODELO OSI vs TCP/IP (encapsulamento)")
osi = ["7 Aplicacao", "6 Apresentacao", "5 Sessao", "4 Transporte",
       "3 Rede", "2 Enlace", "1 Fisica"]
tcpip = ["Aplicacao", "Transporte", "Rede", "Enlace/Fisica"]
print("   OSI:      " + " -> ".join(osi))
print("   TCP/IP:   " + " -> ".join(tcpip))

print("\n6) TCP vs UDP")
print("   TCP: orientado a conexao, confiavel, controle de fluxo (Web, e-mail).")
print("   UDP: sem conexao, rapido, sem garantia (video ao vivo, DNS, jogos).")

print("\n7) PORTAS CONHECIDAS")
portas = {80: "HTTP", 443: "HTTPS", 22: "SSH", 53: "DNS", 3306: "MySQL"}
for p, s in portas.items():
    print(f"   {p} -> {s}")

print("\n8) CHECKSUM (soma de verificacao simples)")
def checksum(dados):
    s = sum(ord(c) for c in dados)
    return s & 0xFFFF
msg = "HELLO"
c = checksum(msg)
print(f"   checksum de '{msg}' = {c} (receptor recalcula e compara)")

print("\n9) ROTEAMENTO: tabela de rotas e proximo salto")
rotas = [("192.168.1.0/24", "direta"), ("10.0.0.0/8", "192.168.1.1"), ("0.0.0.0/0", "192.168.1.254")]
for rede_r, prox in rotas:
    print(f"   {rede_r:<14} -> {prox}")
print("\nOK - redes simuladas com a biblioteca ipaddress.")
'''),
dict(
    stem="Modelagem_de_Dados", name="Modelagem de Dados",
    cat="Banco de Dados", folder="05_Banco_de_Dados", emoji="\U0001F5C4\uFE0F",
    tagline="Modelo conceitual, relacional, cardinalidade, normalização e integridade.",
    about="Da entidade ao banco: modelo conceitual, diagrama ER, cardinalidades, normalização "
          "(1FN/2FN/3FN) e criação do esquema físico com SQLite.",
    examples=r'''
import sqlite3

print("=" * 60)
print("1) MODELO CONCEITUAL (entidades e relacionamentos)")
entidades = ["ALUNO", "DISCIPLINA", "MATRICULA"]
relacoes = [("ALUNO", "MATRICULA", "1:N", "cursa"), ("DISCIPLINA", "MATRICULA", "1:N", "possui")]
for e1, e2, card, nome in relacoes:
    print(f"   {e1} {card} {nome} {e2}")

print("\n2) CARDINALIDADE - tipos")
print("   1:1  -> um para um (ex.: USUARIO - PASSAPORTE)")
print("   1:N  -> um para muitos (ex.: CLIENTE - PEDIDO)")
print("   N:M  -> muitos para muitos (ex.: ALUNO - DISCIPLINA via MATRICULA)")

print("\n3) NORMALIZACAO - tabela com problema (1FN)")
tabela = [("1", "Ana", "Mat1,Mat2"), ("2", "Bruno", "Mat3")]
print("   id | nome | disciplinas (viola 1FN: campo multivalorado)")

print("   Apos 1FN (atomo) + 2FN (sem dependencia parcial) + 3FN (sem transitiva):")
print("   ALUNO(id, nome)  |  MATRICULA(id_aluno, id_disc)  |  DISCIPLINA(id, nome)")

print("\n4) ESQUEMA FISICO com SQLite + consulta com JOIN")
con = sqlite3.connect(":memory:")
cur = con.cursor()
cur.executescript("""
CREATE TABLE aluno (id INTEGER PRIMARY KEY, nome TEXT);
CREATE TABLE disciplina (id INTEGER PRIMARY KEY, nome TEXT);
CREATE TABLE matricula (id_aluno INTEGER, id_disc INTEGER,
    FOREIGN KEY(id_aluno) REFERENCES aluno(id),
    FOREIGN KEY(id_disc) REFERENCES disciplina(id));
INSERT INTO aluno VALUES (1,'Ana'), (2,'Bruno'), (3,'Carla');
INSERT INTO disciplina VALUES (1,'BD'), (2,'Redes'), (3,'SO');
INSERT INTO matricula VALUES (1,1),(1,2),(2,2),(3,3);
""")
print("   Alunos matriculados em Redes:")
for linha in cur.execute("""
    SELECT a.nome, d.nome FROM aluno a
    JOIN matricula m ON m.id_aluno = a.id
    JOIN disciplina d ON d.id = m.id_disc
    WHERE d.nome = 'Redes'"""):
    print("   ", linha)

print("\n5) INTEGRIDADE REFERENCIAL - violacao de FK")
try:
    cur.execute("INSERT INTO matricula VALUES (99, 1)")   # aluno 99 nao existe
except sqlite3.IntegrityError as e:
    print(f"   bloqueado: {e}")

print("\n6) CONSULTA COM AGREGACAO")
print("   Matriculas por disciplina:")
for linha in cur.execute("""
    SELECT d.nome, COUNT(m.id_aluno) FROM disciplina d
    LEFT JOIN matricula m ON m.id_disc = d.id
    GROUP BY d.nome"""):
    print("   ", linha)
print("\nOK - modelagem e SQL demonstrados.")
'''),
dict(
    stem="Programacao_Banco_de_Dados", name="Programação em Banco de Dados",
    cat="Banco de Dados", folder="05_Banco_de_Dados", emoji="\U0001F5E2\uFE0F",
    tagline="SQL básico, joins, agregação, views, procedures, transações e índices.",
    about="Programação com bancos de dados relacionais: DDL, DML, JOINs, agregações, "
          "transações ACID, índices e procedures — tudo executado em SQLite.",
    examples=r'''
import sqlite3

print("=" * 60)
print("1) DDL + DML: criar tabelas e inserir dados")
con = sqlite3.connect(":memory:")
cur = con.cursor()
cur.executescript("""
CREATE TABLE cliente (id INTEGER PRIMARY KEY, nome TEXT, cidade TEXT);
CREATE TABLE pedido (id INTEGER PRIMARY KEY, id_cliente INTEGER,
                     valor REAL, data TEXT,
                     FOREIGN KEY(id_cliente) REFERENCES cliente(id));
INSERT INTO cliente VALUES (1,'Ana','SP'), (2,'Bruno','RJ'), (3,'Carla','SP');
INSERT INTO pedido VALUES (101,1,250.0,'2024-01-10'),
                          (102,1,100.0,'2024-02-05'),
                          (103,2,350.0,'2024-02-20'),
                          (104,3,80.0,'2024-03-01');
""")
print("   tabelas criadas e dados inseridos.")

print("\n2) SELECT com filtro e ordenacao")
for linha in cur.execute("SELECT nome, cidade FROM cliente WHERE cidade = 'SP' ORDER BY nome"):
    print("   ", linha)

print("\n3) JOIN: clientes e seus pedidos")
for linha in cur.execute("""
    SELECT c.nome, p.id, p.valor FROM cliente c
    JOIN pedido p ON p.id_cliente = c.id
    ORDER BY p.valor DESC"""):
    print("   ", linha)

print("\n4) AGREGACAO: total gasto por cliente")
for linha in cur.execute("""
    SELECT c.nome, COUNT(p.id), SUM(p.valor) FROM cliente c
    LEFT JOIN pedido p ON p.id_cliente = c.id
    GROUP BY c.nome ORDER BY 3 DESC"""):
    print("   ", linha)

print("\n5) VIEW: criar visao e consultar")
cur.execute("CREATE VIEW v_total AS SELECT c.nome, SUM(p.valor) total "
            "FROM cliente c JOIN pedido p ON p.id_cliente = c.id GROUP BY c.nome")
for linha in cur.execute("SELECT * FROM v_total"):
    print("   ", linha)

print("\n6) TRANSACAO (ACID): commit e rollback")
try:
    cur.execute("BEGIN")
    cur.execute("INSERT INTO cliente VALUES (4, 'Duda', 'BH')")
    cur.execute("UPDATE pedido SET valor = valor * 1.1 WHERE id = 101")
    con.commit()
    print("   transacao confirmada (commit)")
except Exception as e:
    con.rollback()
    print("   rollback:", e)

print("\n7) INDICE: acelerar busca")
cur.execute("CREATE INDEX idx_pedido_cliente ON pedido(id_cliente)")
print("   indice criado em pedido(id_cliente) -> busca mais rapida em JOINs")
print("   (o SQLite usara o indice automaticamente no plano de execucao)")

print("\n8) PROCEDURE (simulada em SQLite com trigger)")
cur.executescript("""
CREATE TRIGGER trg_pedido AFTER INSERT ON pedido
BEGIN
    UPDATE pedido SET data = date('now') WHERE id = NEW.id AND data IS NULL;
END;
""")
print("   trigger criada: preenche data automaticamente se vazia")

print("\n9) CONSULTA PARAMETRIZADA (evita SQL injection)")
nome_procurado = "Ana"
for linha in cur.execute("SELECT * FROM cliente WHERE nome = ?", (nome_procurado,)):
    print("   ", linha)
print("\nOK - banco de dados programado com SQLite.")
'''),
]