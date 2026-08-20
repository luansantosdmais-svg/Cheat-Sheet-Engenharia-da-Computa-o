# -*- coding: utf-8 -*-
"""PARTE 2B: Programacao (OO, JavaScript, Eng. de Software)."""

SUBJECTS_2B = [
dict(
    stem="Linguagem_Orientada_a_Objetos", name="Linguagem Orientada a Objetos",
    cat="Programação", folder="03_Programacao", emoji="\U0001F40D",
    tagline="Classes, encapsulamento, herança, polimorfismo, composição e exceções.",
    about="Paradigma orientado a objetos aplicado em Python: encapsulamento, herança, "
          "polimorfismo, composição e tratamento de exceções.",
    examples=r'''
print("=" * 60)
print("1) CLASSE + ENCAPSULAMENTO")
class ContaBancaria:
    def __init__(self, titular, saldo=0):
        self.__titular = titular      # privado
        self.__saldo = saldo
    def depositar(self, v):
        if v > 0: self.__saldo += v
    def sacar(self, v):
        if 0 < v <= self.__saldo: self.__saldo -= v
    @property
    def saldo(self):
        return self.__saldo
c = ContaBancaria("Ana", 1000)
c.depositar(250); c.sacar(80)
print(f"   saldo final da {c._ContaBancaria__titular}: R$ {c.saldo:.2f}")

print("\n2) HERANCA + POLIMORFISMO")
class Animal:
    def __init__(self, nome): self.nome = nome
    def som(self): return "..."
class Cachorro(Animal):
    def som(self): return "Au au!"
class Gato(Animal):
    def som(self): return "Miau!"
animais = [Cachorro("Rex"), Gato("Bola")]
for a in animais:
    print(f"   {a.nome}: {a.som()}")

print("\n3) CLASSE ABSTRATA")
from abc import ABC, abstractmethod
class Forma(ABC):
    @abstractmethod
    def area(self): ...
class Circulo(Forma):
    def __init__(self, r): self.r = r
    def area(self): return 3.14159*self.r**2
class Retangulo(Forma):
    def __init__(self, b, h): self.b, self.h = b, h
    def area(self): return self.b*self.h
print(f"   area circulo = {Circulo(2).area():.2f} | area retangulo = {Retangulo(3, 4).area()}")

print("\n4) COMPOSICAO")
class Motor:
    def __init__(self, hp): self.hp = hp
class Carro:
    def __init__(self, modelo, hp):
        self.modelo = modelo
        self.motor = Motor(hp)      # carro TEM-UM motor
    def potencia(self): return self.motor.hp
print(f"   {Carro('Uno', 68).modelo} tem {Carro('Uno', 68).potencia()} cv")

print("\n5) EXCECOES")
class SaldoInsuficiente(Exception): pass
try:
    c.sacar(10000)
    raise SaldoInsuficiente("tentativa de saque acima do saldo")
except SaldoInsuficiente as e:
    print(f"   excecao capturada: {e}")
finally:
    print("   bloco finally executado")

print("\n6) SOBRECARGA DE OPERADOR")
class Vetor2D:
    def __init__(self, x, y): self.x, self.y = x, y
    def __add__(self, o): return Vetor2D(self.x + o.x, self.y + o.y)
    def __mul__(self, k): return Vetor2D(self.x*k, self.y*k)
    def __repr__(self): return f"({self.x}, {self.y})"
print(f"   (2,3) + (4,5) = {Vetor2D(2,3) + Vetor2D(4,5)} | (2,3)*2 = {Vetor2D(2,3)*2}")
print("\nOK - OO demonstrada em Python.")
'''),
dict(
    stem="Desenvolvimento_em_Javascript", name="Desenvolvimento em JavaScript",
    cat="Programação", folder="03_Programacao", emoji="\U0001F4DC",
    tagline="Fundamentos, tipos, funções, arrays, objetos, DOM, assíncrono e ES6+.",
    about="JavaScript moderno executado de verdade (Node.js): tipos e controle, funções de alta "
          "ordem, objetos, desestruturação, async/await e módulos.",
    examples=r'''
import subprocess, textwrap

JS = textwrap.dedent("""
// 1) TIPOS E CONTROLE
const notas = [3.5, 6.0, 8.5];
const status = notas.map(n => n >= 7 ? "Aprovado" : n >= 5 ? "Recuperacao" : "Reprovado");
console.log("1) status por nota:", status.join(" | "));

// 2) ARRAYS - map / filter / reduce
const nums = [1, 2, 3, 4, 5, 6];
console.log("2) pares:", nums.filter(n => n % 2 === 0),
            "| dobrados:", nums.map(n => n * 2),
            "| soma:", nums.reduce((a, b) => a + b, 0));

// 3) OBJETOS + DESESTRUTURACAO + SPREAD
const pessoa = { nome: "Ana", idade: 28, cidade: "SP" };
const { nome, idade } = pessoa;
const copia = { ...pessoa, profissao: "Engenheira" };
console.log("3)", nome, idade, "anos |", JSON.stringify(copia));

// 4) FUNCOES + REST
const soma = (...args) => args.reduce((a, b) => a + b, 0);
console.log("4) soma(1,2,3,4) =", soma(1, 2, 3, 4));

// 5) ASINCRONO - Promise + async/await
const esperar = ms => new Promise(res => setTimeout(res, ms));
(async () => {
    await esperar(10);
    const dados = [3, 1, 4, 1, 5];
    console.log("5) dados ordenados:", dados.sort((a, b) => a - b).join(","));
    console.log("   async/await funcionando.");
})();

// 6) CLASSES (ES6)
class Pilha {
    constructor() { this.itens = []; }
    push(x) { this.itens.push(x); }
    pop()  { return this.itens.pop(); }
    get tamanho() { return this.itens.length; }
}
const p = new Pilha();
["A", "B", "C"].forEach(x => p.push(x));
console.log("6) pilha:", p.pop(), p.pop(), p.pop(), "| tamanho final:", p.tamanho);
""")

r = subprocess.run(["node", "-e", JS], capture_output=True, text=True)
print("=" * 60)
ver = subprocess.run(["node", "--version"], capture_output=True, text=True).stdout.strip().lstrip("v")
print("Executando JavaScript real com Node.js v" + ver + ":")
print()
print(r.stdout)
if r.returncode != 0:
    print("ERRO:", r.stderr)
print("OK - JavaScript executado via Node.js.")
'''),
dict(
    stem="Engenharia_de_Software", name="Engenharia de Software",
    cat="Programação", folder="03_Programacao", emoji="\U0001F3D7\uFE0F",
    tagline="Processos, requisitos, UML, arquitetura, qualidade, testes e CI/CD.",
    about="Práticas e métricas de engenharia de software: pontos de função, complexidade "
          "ciclomática, estimativa COCOMO, PERT e qualidade de código.",
    examples=r'''
import math

print("=" * 60)
print("1) PONTOS DE FUNCAO (estimativa de tamanho)")
# entradas 5, saidas 3, consultas 4, arquivos 6, interfaces 2
pesos = {"baixa": 3, "media": 4, "alta": 6}
entradas, saidas, cons, arq, intf = 5, 3, 4, 6, 2
PF = (entradas*4 + saidas*5 + cons*4 + arq*10 + intf*7)
print(f"   PF brutos = {PF} (ajuste de complexidade pode ser aplicado depois)")

print("\n2) COMPLEXIDADE CICLOMATICA: V(G) = arestas - nos + 2")
arestas, nos = 12, 9
Vg = arestas - nos + 2
print(f"   V(G) = {Vg}  -> caminhos independentes de teste")

print("\n3) ESTIMATIVA COCOMO (organico): PM = a*(KDSI)^b")
KDSI = 10   # milhares de linhas
a_org, b_org = 2.4, 1.05
PM = a_org*(KDSI**b_org)
print(f"   PM = {PM:.1f} pessoas-mes (projeto de {KDSI} KDSI)")

print("\n4) PERT: tempo esperado (otimista, provavel, pessimista)")
o, p, pes = 4, 7, 16
E = (o + 4*pes + p)/6
desvio = (p - o)/6
print(f"   E = {E:.1f} dias | desvio padrao = {desvio:.1f} dias")

print("\n5) DENSIDADE DE DEFEITOS")
defeitos, kloc = 12, 4.5
print(f"   densidade = {defeitos/kloc:.1f} defeitos/KLOC")

print("\n6) METRICAS DE TESTE - piramide")
camadas = {"Unitarios": 70, "Integracao": 20, "E2E": 10}
for k, v in camadas.items():
    print(f"   {k:<10}: {v}%")
print("   (muitos testes unitarios, poucos E2E - teste rapido e barato na base)")

print("\n7) GIT FLOW SIMPLIFICADO")
fluxo = ["main", "feature/funcionalidade", "commit", "pull request", "review", "merge"]
for i, f in enumerate(fluxo, 1):
    print(f"   {i}. {f}")
print("\nOK - metricas e praticas de engenharia de software.")
'''),
]