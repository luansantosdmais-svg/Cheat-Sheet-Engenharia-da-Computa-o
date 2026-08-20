# -*- coding: utf-8 -*-
"""Metadados + exemplos praticos - PARTE 1: Matematica/Ciencias e Hardware."""

SUBJECTS_1 = [
# ===================== MATEMATICA / CIENCIAS =====================
dict(
    stem="Calculo_Diferencial_Integral_I", name="Cálculo Diferencial e Integral I",
    cat="Matemática/Ciências", folder="01_Matematica_e_Ciencias", emoji="\U0001F4D0",
    tagline="Limites, derivadas, aplicações e integrais — o núcleo do Cálculo.",
    about="Fundamento para todas as disciplinas de engenharia. O notebook resolve limites, deriva "
          "funções, traça retas tangentes e calcula integrais com o SymPy, além de gerar o cheat sheet.",
    examples=r'''
%matplotlib inline
import sympy as sp
import matplotlib.pyplot as plt
import numpy as np
x = sp.symbols("x")

print("=" * 60)
print("1) LIMITE: lim (x^2 - 1)/(x - 1) quando x -> 1  (indeterminacao 0/0)")
print("   ->", sp.limit((x**2 - 1)/(x - 1), x, 1))

print("\n2) LIMITE NOTAVEL: lim sen(x)/x quando x -> 0")
print("   ->", sp.limit(sp.sin(x)/x, x, 0))

print("\n3) DERIVADA: f(x) = x^3 * e^x")
f = x**3 * sp.exp(x)
print("   f'  =", sp.diff(f, x))
print("   f'' =", sp.diff(f, x, 2))

print("\n4) REGRA DA CADEIA: h(x) = sen(x^2 + 3x)")
print("   h'  =", sp.diff(sp.sin(x**2 + 3*x), x))

print("\n5) L'HOPITAL: lim (1 - cos(x))/x^2 quando x -> 0")
print("   ->", sp.limit((1 - sp.cos(x))/x**2, x, 0))

print("\n6) INTEGRAL DEFINIDA: Integral de e^x de 0 a 1")
I = sp.integrate(sp.exp(x), (x, 0, 1))
print("   ->", I, "=", I.evalf())

print("\n7) AREA ENTRE CURVAS: y = x^2 e y = sqrt(x) em [0, 1]")
f7, g7 = x**2, sp.sqrt(x)
A = sp.integrate(g7 - f7, (x, 0, 1))
print("   Area =", A, "=", A.evalf())

print("\n8) RETA TANGENTE de f(x) = x^3 - 3x + 2 em x = 1")
f8 = sp.Lambda(x, x**3 - 3*x + 2)
fp8 = sp.diff(f8(x), x)
a = 1
reta = f8(a) + fp8.subs(x, a) * (x - a)
print("   f'(1) =", fp8.subs(x, a), " -> y =", sp.expand(reta))

xx = np.linspace(-2.2, 2.2, 300)
plt.figure(figsize=(7, 4.5))
plt.plot(xx, [float(f8(i)) for i in xx], lw=2.2, color="#147D82", label="f(x) = x^3 - 3x + 2")
tt = np.linspace(-1.5, 2.6, 10)
plt.plot(tt, [float(reta.subs(x, i)) for i in tt], "--", lw=1.8, color="#C97A1A",
         label="reta tangente em x=1")
plt.axhline(0, color="gray", lw=0.8); plt.axvline(0, color="gray", lw=0.8)
plt.scatter([a], [f8(a)], color="#A83E63", zorder=5, s=70)
plt.title("Derivada = inclinacao da reta tangente")
plt.legend(); plt.grid(alpha=.3); plt.tight_layout(); plt.show()

print("\nOK - exemplos resolvidos com SymPy (aritmetica simbolica exata).")
'''),
dict(
    stem="Calculo_II", name="Cálculo II",
    cat="Matemática/Ciências", folder="01_Matematica_e_Ciencias", emoji="\U0001F4C8",
    tagline="Técnicas de integração, impróprias, séries, potências e Taylor.",
    about="Continuação do Cálculo: técnicas de integração avançadas, integrais impróprias, "
          "convergência de séries e aproximação por polinômios de Taylor.",
    examples=r'''
%matplotlib inline
import sympy as sp
import matplotlib.pyplot as plt
import numpy as np
x, n, C = sp.symbols("x n C")

print("=" * 60)
print("1) INTEGRACAO POR PARTES: Integral de x*e^x dx")
print("   ->", sp.integrate(x * sp.exp(x), x) + C)

print("\n2) SUBSTITUICAO TRIGONOMETRICA: Integral de 1/sqrt(9 - x^2) dx")
print("   ->", sp.integrate(1/sp.sqrt(9 - x**2), x) + C)

print("\n3) FRACOES PARCIAIS: Integral de 1/(x^2 - 1) dx")
print("   ->", sp.integrate(1/(x**2 - 1), x) + C)

print("\n4) INTEGRAL IMPROPRIA: Integral de 1/x^2 de 1 a +inf")
print("   ->", sp.integrate(1/x**2, (x, 1, sp.oo)))

print("\n5) p-TESTE: convergencia da serie 1/n^p")
for p in (0.5, 1.0, 1.5, 2.0):
    s = sp.N(sp.Sum(1/n**p, (n, 1, 10000)))
    print(f"   p = {p:.1f}  ->  soma parcial (n=10000) = {float(s):.4f}  "
          f"{'CONVERGE' if p > 1 else 'DIVERGE'}")

print("\n6) SERIE GEOMETRICA: soma de (1/2)^n de 0 a +inf")
print("   ->", sp.Sum((1/2)**n, (n, 0, sp.oo)).doit())

print("\n7) MACLAURIN de e^x (6 termos)")
print("   ", sp.series(sp.exp(x), x, 0, 6).removeO())

xx = np.linspace(-3, 3, 400)
plt.figure(figsize=(7.5, 4.5))
plt.plot(xx, np.exp(xx), lw=2.2, color="k", label="e^x (exata)")
for k, col in ((2, "#C97A1A"), (4, "#A83E63"), (8, "#147D82")):
    s = sp.series(sp.exp(x), x, 0, k + 1).removeO()
    plt.plot(xx, [float(s.subs(x, i)) for i in xx], lw=1.6, color=col,
             label=f"Taylor ordem {k}")
plt.ylim(-2, 12)
plt.title("Polinomios de Taylor aproximam e^x")
plt.legend(); plt.grid(alpha=.3); plt.tight_layout(); plt.show()
print("\nOK - series e integrais resolvidas simbolicamente.")
'''),
dict(
    stem="Metodos_Matematicos", name="Métodos Matemáticos",
    cat="Matemática/Ciências", folder="01_Matematica_e_Ciencias", emoji="\U0001F522",
    tagline="Álgebra linear, EDOs, Fourier, Laplace e ferramentas numéricas.",
    about="Ferramentas matemáticas usadas em engenharia: sistemas lineares, autovalores, equações "
          "diferenciais e séries de Fourier com NumPy e SymPy.",
    examples=r'''
%matplotlib inline
import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
from scipy.integrate import odeint

print("=" * 60)
print("1) SISTEMA LINEAR: 2x + y = 5 ; x - 3y = -1")
A = np.array([[2, 1], [1, -3]])
b = np.array([5, -1])
x = np.linalg.solve(A, b)
print("   x =", x[0].round(4), " y =", x[1].round(4))

print("\n2) AUTOVALORES/AUTOVETORES de [[4, 1], [2, 3]]")
w, v = np.linalg.eig(np.array([[4, 1], [2, 3]]))
print("   autovalores:", w.round(4))
print("   autovetores (colunas):\n", v.round(4))

print("\n3) ROTACAO DE 45 GRAUS no vetor [1, 0]")
th = np.radians(45)
R = np.array([[np.cos(th), -np.sin(th)], [np.sin(th), np.cos(th)]])
print("   R(45) =\n", R.round(4))
print("   R * [1,0] =", (R @ np.array([1., 0.])).round(4))

print("\n4) EDO: y'' + y = 0, y(0)=1, y'(0)=0  ->  y = cos(t)")
t = sp.symbols("t")
y = sp.Function("y")
edo = sp.Eq(sp.diff(y(t), t, 2) + y(t), 0)
sol = sp.dsolve(edo, y(t), ics={y(0): 1, sp.diff(y(t), t).subs(t, 0): 0})
print("   solucao:", sol)

print("\n5) SERIE DE FOURIER de f(t) = |t| em [-pi, pi]")
def fourier(tv, N=10):
    out = np.pi/2
    for k in range(1, N + 1):
        out += (-4/np.pi) * np.cos((2*k - 1)*tv)/(2*k - 1)**2
    return out
tt = np.linspace(-np.pi, np.pi, 800)
plt.figure(figsize=(7.5, 4.2))
plt.plot(tt, np.abs(tt), "k--", lw=2, label="|t| (original)")
for N, col in ((2, "#C97A1A"), (6, "#A83E63"), (30, "#147D82")):
    plt.plot(tt, fourier(tt, N), lw=1.4, color=col, label=f"{N} harmonicos")
plt.title("Aproximacao de Fourier de |t|")
plt.legend(); plt.grid(alpha=.3); plt.tight_layout(); plt.show()
print("\nOK - algebra linear, EDOs e Fourier com NumPy/SymPy.")
'''),
dict(
    stem="Fisica_Geral_Experimental_Mecanica_Energia",
    name="Física Geral Experimental — Mecânica & Energia",
    cat="Matemática/Ciências", folder="01_Matematica_e_Ciencias", emoji="\U0000269B\uFE0F",
    tagline="Cinemática, leis de Newton, trabalho, energia, momento e rotação.",
    about="Mecânica clássica aplicada: movimento, forças, conservação de energia e colisões, "
          "com simulações numéricas e gráficos.",
    examples=r'''
%matplotlib inline
import numpy as np
import matplotlib.pyplot as plt

g = 9.81

print("=" * 60)
print("1) MRUV: carro de 0 a 100 km/h em 8 s")
v0, vf, dt = 0.0, 100/3.6, 8.0
a = (vf - v0)/dt
d = v0*dt + 0.5*a*dt**2
print(f"   aceleracao = {a:.2f} m/s^2 | distancia = {d:.1f} m")

print("\n2) QUEDA LIVRE do repouso, 45 m")
h = 45.0
v = np.sqrt(2*g*h)
tq = np.sqrt(2*h/g)
print(f"   v_final = {v:.2f} m/s | tempo = {tq:.2f} s")

print("\n3) TRABALHO / ENERGIA: bloco de 10 kg em plano inclinado 30 graus")
m = 10.0
theta = np.radians(30)
W = m*g*10*np.cos(theta)
K = W
v_energia = np.sqrt(2*K/m)
print(f"   trabalho da forca paralela (10 m) = {W:.1f} J | v (sem atrito) = {v_energia:.2f} m/s")

print("\n4) COLISAO INELASTICA: m1=2kg v1=6m/s ; m2=4kg v2=0")
m1, v1, m2, v2 = 2.0, 6.0, 4.0, 0.0
v_apos = (m1*v1 + m2*v2)/(m1 + m2)
print(f"   v' = {v_apos:.2f} m/s (conservacao de momento)")

print("\n5) LANCAMENTO DE PROJETIL: v0=30 m/s, angulo 45 graus")
v0, ang = 30.0, np.radians(45)
t_total = 2*v0*np.sin(ang)/g
alcance = v0*np.cos(ang)*t_total
altura = (v0*np.sin(ang))**2/(2*g)
print(f"   tempo total = {t_total:.2f} s | alcance = {alcance:.1f} m | altura max = {altura:.1f} m")

ts = np.linspace(0, t_total, 200)
x_t = v0*np.cos(ang)*ts
y_t = v0*np.sin(ang)*ts - 0.5*g*ts**2
plt.figure(figsize=(7, 4.5))
plt.plot(x_t, y_t, color="#147D82", lw=2)
plt.axhline(0, color="gray", lw=0.8)
plt.scatter([alcance], [0], color="#A83E63", s=60, label="alcance")
plt.title("Trajetoria de um projetil (sem resistencia do ar)")
plt.xlabel("distancia (m)"); plt.ylabel("altura (m)")
plt.legend(); plt.grid(alpha=.3); plt.tight_layout(); plt.show()
print("\nOK - cinematica e dinamica simuladas numericamente.")
'''),
dict(
    stem="Principios_Eletricidade_Magnetismo", name="Princípios de Eletricidade e Magnetismo",
    cat="Matemática/Ciências", folder="01_Matematica_e_Ciencias", emoji="\U000026A1",
    tagline="Carga, força de Coulomb, campo elétrico, potencial, circuitos e indução.",
    about="Fundamentos do eletromagnetismo: interação entre cargas, campos, potencial, circuitos "
          "RC e indução, com cálculos e gráficos de campo.",
    examples=r'''
%matplotlib inline
import numpy as np
import matplotlib.pyplot as plt

k = 8.9875e9

print("=" * 60)
print("1) LEI DE COULOMB: duas cargas de 1 uC separadas por 0,5 m")
q1, q2, r = 1e-6, 1e-6, 0.5
F = k*q1*q2/r**2
print(f"   F = {F:.3f} N (repulsiva, cargas iguais)")

print("\n2) CAMPO ELETRICO de carga q = 2 nC a 1 m de distancia")
q, r2 = 2e-9, 1.0
E = k*q/r2**2
print(f"   E = {E:.1f} N/C")

print("\n3) POTENCIAL: V = k*q/r (mesma carga)")
print(f"   V = {k*q/r2:.1f} V")

print("\n4) CIRCUITO RC: carga do capacitor, R=1 kOhm, C=100 uF, V=12 V")
R, C, V = 1e3, 100e-6, 12.0
tau = R*C
t_charg = np.linspace(0, 5*tau, 300)
Q = C*V*(1 - np.exp(-t_charg/tau))
Vc = V*(1 - np.exp(-t_charg/tau))
print(f"   tau = {tau*1000:.1f} ms | carga final = {C*V*1e6:.1f} uC")

fig, ax = plt.subplots(1, 2, figsize=(9.5, 3.8))
ax[0].plot(t_charg*1e3, Vc, color="#147D82", lw=2)
ax[0].set_title("Carga do capacitor (RC)"); ax[0].set_xlabel("t (ms)"); ax[0].set_ylabel("Vc (V)")
ax[0].grid(alpha=.3)

print("\n5) FORCA DE LORENTZ: F = q*v*B (v perpendicular a B)")
q, v, B = 1.6e-19, 2e6, 0.5
print(f"   F = {q*v*B:.3e} N")

print("\n6) LINHAS DE CAMPO de uma carga positiva (2D)")
x2 = np.linspace(-2, 2, 15); y2 = np.linspace(-2, 2, 15)
X, Y = np.meshgrid(x2, y2)
R2 = np.sqrt(X**2 + Y**2) + 1e-6
Ex = k*q1/X.shape[0]*0 + X/R2**3   # campo de carga q na origem (escala arbitraria)
Ey = Y/R2**3
ax[1].streamplot(X, Y, Ex, Ey, color="#C97A1A", density=1.2)
ax[1].set_title("Campo de carga positiva"); ax[1].set_xlabel("x"); ax[1].set_ylabel("y")
plt.tight_layout(); plt.show()
print("\nOK - eletricidade e magnetismo calculados numericamente.")
'''),
dict(
    stem="Resistencia_dos_Materiais", name="Resistência dos Materiais",
    cat="Matemática/Ciências", folder="01_Matematica_e_Ciencias", emoji="\U0001F3D7\uFE0F",
    tagline="Tensão, deformação, esforços internos, torção, flexão e flambagem.",
    about="Comportamento mecânico de materiais e estruturas: tensão-deformação, lei de Hooke, "
          "diagramas de esforços, deflexão de vigas e flambagem.",
    examples=r'''
%matplotlib inline
import numpy as np
import matplotlib.pyplot as plt

print("=" * 60)
print("1) TENSAO NORMAL: barra de 20 mm x 10 mm sob 50 kN")
A = 20e-3 * 10e-3
P = 50e3
sigma = P/A
print(f"   A = {A*1e4:.1f} cm^2 | sigma = {sigma/1e6:.1f} MPa")

print("\n2) LEI DE HOOKE: deformacao do aco (E = 200 GPa)")
E_aco = 200e9
eps = sigma/E_aco
delta = eps * 2.0   # barra de 2 m
print(f"   epsilon = {eps*1e6:.1f} ustrain | alongamento = {delta*1e3:.2f} mm")

print("\n3) TORCAO: eixo macico de 40 mm, T = 1 kN.m")
d, T = 40e-3, 1e3
J = np.pi*d**4/32
tau_max = T*(d/2)/J
print(f"   J = {J*1e8:.2f} cm^4 | tau_max = {tau_max/1e6:.1f} MPa")

print("\n4) MOMENTO DE INERCIA de viga retangular b=0.2 h=0.3 (eixo x)")
b, h = 0.2, 0.3
Ix = b*h**3/12
print(f"   Ix = {Ix*1e4:.2f} cm^4")

print("\n5) FLAMBAGEM DE EULER: coluna biarticulada L=3 m, E=200 GPa")
L = 3.0
Im = b*h**3/12
Pcr = np.pi**2*E_aco*Im/L**2
print(f"   Pcr = {Pcr/1e3:.1f} kN")

print("\n6) DEFLEXAO de viga biapoiada com carga concentrada central")
Lv, Pv, Ev, Iv = 4.0, 20e3, 200e9, Ix
dmax = Pv*Lv**3/(48*Ev*Iv)
print(f"   deflexao maxima = {dmax*1e3:.2f} mm")

xx = np.linspace(0, Lv, 300)
y_def = Pv*Lv**3/(48*Ev*Iv) * (3*(xx/Lv) - 4*(xx/Lv)**3)  # x <= L/2 (simetria)
y_def_full = np.concatenate([y_def[:150][::-1], y_def[:150]])
plt.figure(figsize=(7, 3.6))
plt.plot(np.concatenate([xx[:150][::-1], xx[:150]]), y_def_full*1e3, color="#147D82", lw=2)
plt.axhline(0, color="gray", lw=0.8)
plt.title("Linha elastica - viga biapoiada (carga central)")
plt.xlabel("x (m)"); plt.ylabel("deflexao (mm)")
plt.grid(alpha=.3); plt.tight_layout(); plt.show()
print("\nOK - resistencias calculadas com formulas classicas.")
'''),
# ============================ HARDWARE ============================
dict(
    stem="Arquitetura_Organizacao_Computadores", name="Arquitetura e Organização de Computadores",
    cat="Hardware", folder="02_Hardware", emoji="\U0001F5A5\uFE0F",
    tagline="Representação de dados, CPU/ISA, memória & cache, E/S e barramentos.",
    about="Como o hardware representa dados e executa instruções: bases numéricas, complemento de 2, "
          "IEEE 754, ciclo de instrução, cache e métricas de desempenho.",
    examples=r'''
import struct

print("=" * 60)
print("1) BASES: converter 173 decimal")
n = 173
print(f"   173 = 0b{bin(n)[2:]} (binario) = 0x{hex(n)[2:].upper()} (hex)")
print(f"   hex -> 4 bits por digito: 0xAD = 1010 1101")

print("\n2) COMPLEMENTO DE 2 (8 bits): representar -42")
x = 42
c2 = (1 << 8) - x
print(f"   42  = 0b{bin(x)[2:]:>08s}")
print(f"   -42 = 0b{bin(c2)[2:]:>08s}  (= 11111111 - 42 + 1)")

print("\n3) SOMAR COM OVERFLOW (8 bits): 100 + 60")
soma = 100 + 60
print(f"   100 + 60 = {soma} -> em 8 bits: {soma & 0xFF} (overflow! carry descartado)")

print("\n4) IEEE 754 (float 32 bits): representacao de -6.5")
b = struct.pack(">f", -6.5)
bits = "".join(f"{byte:08b}" for byte in b)
print(f"   bits: {bits}")
print(f"   sinal={bits[0]} | expoente={int(bits[1:9],2)} (bias 127) | mantissa={bits[9:]}")

print("\n5) TEMPO DE CPU: IC = 2e9, CPI = 1.5, f = 3 GHz")
IC, CPI, f = 2e9, 1.5, 3e9
t_cpu = IC*CPI/f
print(f"   Tempo = {t_cpu:.3f} s")

print("\n6) CACHE - AMAT com taxa de miss de 5%")
t_hit, miss, t_miss = 1e-9, 0.05, 100e-9
amat = t_hit + miss*t_miss
print(f"   AMAT = {amat*1e9:.1f} ns")

print("\n7) PIPELINE: 5 estagios, 100 instrucoes, clock 2 GHz")
n_ins, estagios = 100, 5
t_sem = n_ins*estagios/(2e9)
t_com = (n_ins + estagios - 1)/(2e9)
print(f"   sem pipeline = {t_sem*1e9:.0f} ns | com pipeline = {t_com*1e9:.0f} ns "
      f"| speedup = {t_sem/t_com:.1f}x")
print("\nOK - numeros, IEEE754 e desempenho simulados em Python.")
'''),
dict(
    stem="Arquiteturas_Paralelas_Distribuidas", name="Arquiteturas Paralelas e Distribuídas",
    cat="Hardware", folder="02_Hardware", emoji="\U0001F310",
    tagline="Paralelismo, sincronização, sistemas distribuídos, consistência e escala.",
    about="Computação paralela e distribuída: lei de Amdahl, threads, race conditions, latência "
          "de rede e trade-offs de consistência.",
    examples=r'''
%matplotlib inline
import threading
import time
import numpy as np
import matplotlib.pyplot as plt
from concurrent.futures import ThreadPoolExecutor

print("=" * 60)
print("1) LEI DE AMDALH: speedup maximo vs fracao paralela")
def amdahl(fr_par, p):
    return 1/((1 - fr_par) + fr_par/p)
print(f"   50% paralelo, 8 nucleos: S = {amdahl(0.5, 8):.2f}x")
print(f"   95% paralelo, 8 nucleos: S = {amdahl(0.95, 8):.2f}x")
print(f"   95% paralelo, 64 nucleos: S = {amdahl(0.95, 64):.2f}x")

procs = np.arange(1, 33)
plt.figure(figsize=(6.5, 4))
for frac, col, lbl in ((0.5, "#C97A1A", "50% paralelo"), (0.9, "#A83E63", "90% paralelo"),
                       (0.99, "#147D82", "99% paralelo")):
    plt.plot(procs, [amdahl(frac, p) for p in procs], lw=2, color=col, label=lbl)
plt.plot(procs, procs, "k--", lw=1, label="speedup ideal")
plt.title("Lei de Amdahl"); plt.xlabel("processadores"); plt.ylabel("speedup")
plt.legend(); plt.grid(alpha=.3); plt.tight_layout(); plt.show()

print("\n2) SOMA PARALELA com ThreadPoolExecutor")
def soma_par(vet, n_threads=4):
    with ThreadPoolExecutor(n_threads) as ex:
        partes = list(ex.map(lambda c: sum(c), np.array_split(vet, n_threads)))
    return sum(partes)
vet = np.arange(1, 1_000_001)
print(f"   soma serial  = {sum(vet)}")
print(f"   soma paralela= {soma_par(vet)}  (iguais: {sum(vet) == soma_par(vet)})")

print("\n3) RACE CONDITION: contador sem lock vs com lock")
contador = {"v": 0}
def inc(sem_lock, n=100000):
    for _ in range(n):
        if sem_lock is None:
            contador["v"] += 1
        else:
            with sem_lock:
                contador["v"] += 1
ths = [threading.Thread(target=inc, args=(None,)) for _ in range(8)]
for t in ths: t.start()
for t in ths: t.join()
print(f"   sem lock: esperado=800000, obtido={contador['v']}  -> RACE CONDITION")

contador["v"] = 0
lk = threading.Lock()
ths = [threading.Thread(target=inc, args=(lk,)) for _ in range(8)]
for t in ths: t.start()
for t in ths: t.join()
print(f"   com lock: esperado=800000, obtido={contador['v']}  -> OK")

print("\n4) LATENCIA vs LARGURA DE BANDA")
lat, bw = 0.1, 1000   # ms e Mbps
tamanhos = [100, 1000, 10000]   # KB
for kb in tamanhos:
    t_transf = kb*8e3/bw   # ms
    print(f"   {kb:>6} KB -> tempo = {t_transf:.2f} ms (latencia {lat} ms)")
print("\nOK - paralelismo e distribuicao demonstrados.")
'''),
dict(
    stem="Circuitos_Eletricos", name="Circuitos Elétricos",
    cat="Hardware", folder="02_Hardware", emoji="\U0001F50C",
    tagline="Ohm, associações, Kirchhoff, transitórios, CA e potência.",
    about="Análise de circuitos: leis de Ohm e Kirchhoff, teoremas de Thévenin/Norton, resposta "
          "transitória RC/RL e circuitos em corrente alternada com fasores.",
    examples=r'''
%matplotlib inline
import numpy as np
import matplotlib.pyplot as plt

print("=" * 60)
print("1) LEI DE OHM: R = 10 Ohm, I = 2 A")
V = 10*2
print(f"   V = {V} V | P = {V*2} W")

print("\n2) ASSOCIACOES")
R1, R2, R3 = 10.0, 20.0, 30.0
Rs = R1 + R2 + R3
Rp = 1/(1/R1 + 1/R2 + 1/R3)
print(f"   serie: {Rs:.1f} ohm | paralelo: {Rp:.2f} ohm")

print("\n3) DIVISOR DE TENSAO: V = 12 V com R1=1k e R2=3k")
V_s, R_a, R_b = 12.0, 1e3, 3e3
Vb = V_s*R_b/(R_a + R_b)
print(f"   V sobre R2 = {Vb:.2f} V")

print("\n4) KIRCHHOFF (analise de malhas) com numpy")
# malha 1: 10*i1 + 5*(i1-i2) = 12 ; malha 2: 5*(i2-i1) + 15*i2 = -6
A = np.array([[15, -5], [-5, 20]])
B = np.array([12, -6])
i = np.linalg.solve(A, B)
print(f"   i1 = {i[0]:.3f} A | i2 = {i[1]:.3f} A")

print("\n5) THEVENIN: Vth e Rth vistos pela carga")
V_src, R_th = 12.0, 50.0
for Rl in (25, 50, 100):
    Il = V_src/(R_th + Rl)
    print(f"   Rl = {Rl:>3} ohm -> Il = {Il*1000:.1f} mA | P = {Il**2*Rl:.2f} W")
print("   (maxima potencia quando Rl = Rth = 50 ohm)")

print("\n6) TRANSITORIO RC: carga de 1 kOhm . 100 uF em 12 V")
R, C, Vf = 1e3, 100e-6, 12.0
tau = R*C
t = np.linspace(0, 5*tau, 300)
vc = Vf*(1 - np.exp(-t/tau))
ic = (Vf/R)*np.exp(-t/tau)
fig, ax = plt.subplots(1, 2, figsize=(9.5, 3.6))
ax[0].plot(t*1e3, vc, color="#147D82", lw=2); ax[0].set_title("vC(t) - carga RC")
ax[0].set_xlabel("t (ms)"); ax[0].set_ylabel("Vc (V)"); ax[0].grid(alpha=.3)
ax[1].plot(t*1e3, ic*1e3, color="#A83E63", lw=2); ax[1].set_title("iC(t) - corrente")
ax[1].set_xlabel("t (ms)"); ax[1].set_ylabel("i (mA)"); ax[1].grid(alpha=.3)
plt.tight_layout(); plt.show()

print("\n7) CORRENTE ALTERNADA: fasores, RLC serie (f = 60 Hz)")
f_ca, L, Cv = 60.0, 0.1, 50e-6
w = 2*np.pi*f_ca
ZL, ZC = 1j*w*L, 1/(1j*w*Cv)
Z = 100 + ZL + ZC
Vrms = 127
I = Vrms/Z
print(f"   Z = {abs(Z):.1f} ohm ang({np.degrees(np.angle(Z)):.1f}°)")
print(f"   I = {abs(I):.3f} A | FP = cos(phi) = {np.cos(np.angle(Z)):.3f}")
print("\nOK - circuitos analisados com numpy.")
'''),
dict(
    stem="Eletronica_Analogica", name="Eletrônica Analógica",
    cat="Hardware", folder="02_Hardware", emoji="\U0001F3A7",
    tagline="Diodos, BJT, MOSFET, amplificadores e amp-op.",
    about="Dispositivos semicondutores e amplificadores: diodos e retificadores, polarização de "
          "transistores, ganho de amp-ops e resposta em frequência.",
    examples=r'''
%matplotlib inline
import numpy as np
import matplotlib.pyplot as plt

print("=" * 60)
print("1) DIODO: retificacao de meia onda (Vp = 12 V)")
Vp, R = 12.0, 1000.0
Vdc = Vp/np.pi
print(f"   valor medio = {Vdc:.2f} V | valor eficaz (meia onda) = {Vp/2:.2f} V")

t = np.linspace(0, 0.05, 1000)
vin = Vp*np.sin(2*np.pi*60*t)
vout = np.maximum(vin - 0.7, 0)   # queda de 0.7 V no silicio
plt.figure(figsize=(7, 3.8))
plt.plot(t*1e3, vin, color="#888", lw=1.2, label="vin")
plt.plot(t*1e3, vout, color="#147D82", lw=2, label="vout (meia onda)")
plt.title("Retificador de meia onda (queda de 0,7 V)"); plt.xlabel("t (ms)")
plt.ylabel("V"); plt.legend(); plt.grid(alpha=.3); plt.tight_layout(); plt.show()

print("\n2) POLARIZACAO BJT: Vcc=12 V, Rb=470k, Rc=1k, beta=150")
Vcc, Rb, Rc, beta = 12.0, 470e3, 1e3, 150
Ib = (Vcc - 0.7)/Rb
Ic = beta*Ib
Vce = Vcc - Ic*Rc
print(f"   Ib = {Ib*1e6:.1f} uA | Ic = {Ic*1e3:.1f} mA | Vce = {Vce:.2f} V "
      f"({'ATIVO' if 0.2 < Vce < Vcc else 'SATURADO/CORTE'})")

print("\n3) AMPLIFICADOR INVERSOR: Rf = 10k, Rin = 1k")
Rf, Rin = 10e3, 1e3
Av = -Rf/Rin
print(f"   Av = {Av} (ganho de tensao)")
print("\n   NAO INVERSOR: Rf = 9k, R1 = 1k")
Av2 = 1 + 9e3/1e3
print(f"   Av = {Av2}")

print("\n4) SOMADOR: vo = -Rf*(v1/R1 + v2/R2)")
v1, v2 = 1.0, 2.0
vo = -10e3*(v1/5e3 + v2/10e3)
print(f"   vo = {vo:.2f} V")

print("\n5) FILTRO RC passa-baixa: resposta em frequencia")
fc = 1/(2*np.pi*1e3*100e-9)
f = np.logspace(1, 6, 400)
H = 1/np.sqrt(1 + (f/fc)**2)
plt.figure(figsize=(7, 3.8))
plt.semilogx(f, 20*np.log10(H), color="#A83E63", lw=2)
plt.axhline(-3, color="k", ls="--", lw=1); plt.axvline(fc, color="gray", ls="--", lw=1)
plt.title("Filtro passa-baixa RC (freq. de corte = 1,59 kHz)")
plt.xlabel("f (Hz)"); plt.ylabel("ganho (dB)"); plt.grid(alpha=.3, which="both")
plt.tight_layout(); plt.show()
print("\nOK - semicondutores e amplificadores analisados.")
'''),
]