import streamlit as st
import graphviz
from fractions import Fraction

# Función para formatear fracciones en LaTeX
def f2l(f):
    if f.denominator == 1:
        return str(f.numerator)
    return f"\\frac{{{f.numerator}}}{{{f.denominator}}}"

st.set_page_config(page_title="Generador de Examen Estocásticos", layout="wide")

st.title(" Resolución Interactiva: Procesos Estocásticos")
st.markdown("Ingresa un número de cuenta. La aplicación resolverá el examen paso a paso mostrando la teoría y te entregará el código LaTeX completo listo para compilar.")

cuenta = st.text_input("Ingresa el número de cuenta (mínimo 6 dígitos Max 9 dígitos):", "424104976")

if st.button("Generar Solución y LaTeX"):
    if len(cuenta) >= 6 and cuenta.isdigit():
        # ==========================================
        # 1. EXTRACCIÓN Y CÁLCULOS MATEMÁTICOS
        # ==========================================
        a1, a2, a3, a4, a5, a6 = [int(cuenta[i]) for i in range(6)]
        
        p1 = Fraction(a1 + 1, a1 + a2 + 2)
        p2 = Fraction(a2 + 1, a1 + a2 + 2)
        p3 = Fraction(a3 + 1, a3 + a4 + 2)
        p4 = Fraction(a4 + 1, a3 + a4 + 2)
        p5 = Fraction(a5 + 1, a5 + a6 + 2)
        p6 = Fraction(a6 + 1, a5 + a6 + 2)
        
        p2_11 = p1 * p1
        p2_12 = p1 * p2 + p2 * p3
        p2_13 = p2 * p4
        
        p2_21 = p4 * p5
        p2_22 = p3 * p3
        p2_23 = p3 * p4 + p4 * p6
        
        p2_31 = p5 * p1 + p6 * p5
        p2_32 = p5 * p2
        p2_33 = p6 * p6

        k3 = p2 / p5
        k2 = p2 / p4
        sum_k = 1 + k2 + k3
        pi1 = Fraction(1, sum_k)
        pi2 = k2 * pi1
        pi3 = k3 * pi1
        
        e_tau = Fraction(1, p4)

        # ==========================================
        # 2. VISTA INTERACTIVA EN STREAMLIT
        # ==========================================
        st.success(f"¡Cálculos completados para el número de cuenta: {cuenta}!")
        st.divider()

        st.header("Definición Preliminar del Espacio de Probabilidad")
        st.markdown(r"Sea $(\Omega, \mathcal{F}, \mathbb{P})$ un espacio de probabilidad y $I = \{1, 2, 3\}$ un espacio de estados finito dotado de la $\sigma$-álgebra discreta $\mathcal{P}(I)$. Definimos el proceso estocástico $X = (X_n)_{n \in \mathbb{N}_0}$ adaptado a su filtración natural $\mathcal{F}_n = \sigma(X_0, \dots, X_n)$.")
        st.markdown(f"Evaluando los escalares del número de cuenta proporcionado: **$a_1={a1}, a_2={a2}, a_3={a3}, a_4={a4}, a_5={a5}, a_6={a6}$**.")

        st.header("Ejercicio 1")
        st.markdown("**Pregunta:** Considere la matriz que acaba de construir.\na) Demuestre que $p_1+p_2=1$, $p_3+p_4=1$, $p_5+p_6=1$. Deduzca que la matriz P es estocástica. Calcule explícitamente P usando su número de cuenta.")
        st.info("**Definición (Matriz Estocástica):** Una matriz $P = (p_{ij})_{i,j \in I}$ se denomina matriz estocástica (o matriz de transición de Markov) si satisface:\n1. $p_{ij} \ge 0$ para todo $i, j \in I$.\n2. $\sum_{j \in I} p_{ij} = 1$ para todo $i \in I$.")
        st.markdown("Procedemos a sustituir los valores de los escalares $a_k$ en las fórmulas para los coeficientes del núcleo de transición de Markov:")
        st.latex(rf"""
        \begin{{aligned}}
        p_1 &= \frac{{{a1}+1}}{{{a1}+{a2}+2}} = {f2l(p1)}, \quad p_2 = \frac{{{a2}+1}}{{{a1}+{a2}+2}} = {f2l(p2)} \\
        p_3 &= \frac{{{a3}+1}}{{{a3}+{a4}+2}} = {f2l(p3)}, \quad p_4 = \frac{{{a4}+1}}{{{a3}+{a4}+2}} = {f2l(p4)} \\
        p_5 &= \frac{{{a5}+1}}{{{a5}+{a6}+2}} = {f2l(p5)}, \quad p_6 = \frac{{{a6}+1}}{{{a5}+{a6}+2}} = {f2l(p6)}
        \end{{aligned}}
        """)
        st.markdown(f"Comprobamos que las sumas por fila son exactamente 1:\n* **Fila 1:** ${f2l(p1)} + {f2l(p2)} = 1$\n* **Fila 2:** ${f2l(p3)} + {f2l(p4)} = 1$\n* **Fila 3:** ${f2l(p5)} + {f2l(p6)} = 1$")
        st.latex(rf"P = \begin{{pmatrix}} {f2l(p1)} & {f2l(p2)} & 0 \\ 0 & {f2l(p3)} & {f2l(p4)} \\ {f2l(p5)} & 0 & {f2l(p6)} \end{{pmatrix}}")

        st.header("Ejercicio 2")
        st.markdown("**Pregunta:** Considere la cadena de Markov con matriz de transición P.\na) Dibuje el grafo de transición.\nb) Determine las clases de comunicación.\nc) Estudie si la cadena es irreducible.")
        st.markdown("**a) Grafo de transición:** El soporte del núcleo de transición nos indica las aristas del grafo dirigido.")
        
        # Grafo dinámico usando Graphviz
        grafo = graphviz.Digraph()
        grafo.attr(rankdir='LR')
        grafo.node('1', '1', shape='circle')
        grafo.node('2', '2', shape='circle')
        grafo.node('3', '3', shape='circle')
        grafo.edge('1', '1', label=f2l(p1))
        grafo.edge('1', '2', label=f2l(p2))
        grafo.edge('2', '2', label=f2l(p3))
        grafo.edge('2', '3', label=f2l(p4))
        grafo.edge('3', '1', label=f2l(p5))
        grafo.edge('3', '3', label=f2l(p6))
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.graphviz_chart(grafo)

        st.markdown("**b) y c) Clases de comunicación e Irreducibilidad:**")
        st.info("**Definición:** Decimos que el estado $j$ es accesible desde $i$ ($i \to j$) si existe un $n \ge 0$ tal que $P^n(i,j) > 0$. Dos estados se comunican ($i \leftrightarrow j$) si $i \to j$ y $j \to i$. Una cadena de Markov es **irreducible** si todos sus estados pertenecen a una única clase de comunicación.")
        
        st.markdown("A partir de las probabilidades de transición en un paso ($n=1$), observamos las siguientes rutas directas:")
        st.markdown(f"""
        * $1 \\to 2$ (pues $P_{{12}} = {f2l(p2)} > 0$)
        * $2 \\to 3$ (pues $P_{{23}} = {f2l(p4)} > 0$)
        * $3 \\to 1$ (pues $P_{{31}} = {f2l(p5)} > 0$)
        """)
        
        st.markdown(f"Dado que podemos establecer el ciclo $1 \\to 2 \\to 3 \\to 1$, podemos transitar de cualquier estado a cualquier otro en un número finito de pasos. Por ejemplo, para ir de 1 a 3, usamos la ruta $1 \\to 2 \\to 3$ en $n=2$ pasos, asegurando que $P^2_{{13}} > 0$. \n\nDado que el grafo dirigido asociado es fuertemente conexo, todos los estados se comunican entre sí. Concluimos que la cadena es **irreducible** y posee una única clase de comunicación: $C=\\{{1,2,3\\}}$.")

        st.header("Ejercicio 3")
        st.markdown("**Pregunta:** Calcule la matriz $P^2$ e interprete probabilísticamente las entradas de $P^2$. Además, determine $\mathbb{P}(X_2=3|X_0=1)$.")
        st.info("**Teorema (Ecuaciones de Chapman-Kolmogorov):** Para cualesquiera estados $i, j$ y tiempos $n, m \ge 0$, la probabilidad de transición a $n+m$ pasos satisface: $P^{n+m}_{ij} = \sum_{k \in I} P^n_{ik} P^m_{kj}$. En notación matricial, $P^{n+m} = P^n P^m$.")
        st.markdown("Calculamos la matriz $P^2$ y desarrollamos el producto algebraico explícitamente:")
        st.latex(rf"""
        \begin{{aligned}}
        (P^2)_{{11}} &= \left({f2l(p1)}\right)\left({f2l(p1)}\right) + \left({f2l(p2)}\right)(0) + (0)\left({f2l(p5)}\right) = {f2l(p2_11)} \\
        (P^2)_{{12}} &= \left({f2l(p1)}\right)\left({f2l(p2)}\right) + \left({f2l(p2)}\right)\left({f2l(p3)}\right) + (0)(0) = {f2l(p2_12)} \\
        (P^2)_{{13}} &= \left({f2l(p1)}\right)(0) + \left({f2l(p2)}\right)\left({f2l(p4)}\right) + (0)\left({f2l(p6)}\right) = {f2l(p2_13)}
        \end{{aligned}}
        """)
        st.latex(rf"P^2 = \begin{{pmatrix}} {f2l(p2_11)} & {f2l(p2_12)} & {f2l(p2_13)} \\ {f2l(p2_21)} & {f2l(p2_22)} & {f2l(p2_23)} \\ {f2l(p2_31)} & {f2l(p2_32)} & {f2l(p2_33)} \end{{pmatrix}}")
        st.markdown(f"**Interpretación probabilística:** Cada entrada $(P^2)_{{ij}}$ representa la suma de las probabilidades de todas las trayectorias posibles de longitud exacta $n=2$ que comienzan en el estado $i$ y terminan en el estado $j$. Es decir, es la probabilidad de transición condicional $\mathbb{{P}}(X_2 = j \mid X_0 = i)$.\n\nPara el caso particular solicitado:\n$\mathbb{{P}}(X_2 = 3 \mid X_0 = 1) = (P^2)_{{13}} = {f2l(p2_13)} \\approx {float(p2_13):.4f}$.\n\nNotemos que la única ruta posible en 2 pasos para ir de 1 a 3 es la trayectoria $1 \\to 2 \\to 3$, cuya probabilidad es exactamente $P_{{12}} \\times P_{{23}} = ({f2l(p2)}) \\times ({f2l(p4)}) = {f2l(p2_13)}$.")

        st.header("Ejercicio 4")
        st.markdown("**Pregunta:** Sea $\pi=(\pi_1,\pi_2,\pi_3)$. Resuelva $\pi P = \pi$ con la condición $\pi_1+\pi_2+\pi_3=1$. Obtenga la distribución estacionaria correspondiente a su número de cuenta.")
        st.info("""**Teorema de Perron-Frobenius para Matrices Estocásticas:** Sea $P$ una matriz estocástica de dimensión $N \\times N$ correspondiente a una cadena de Markov finita e irreducible. Entonces:
1. El radio espectral de $P$ es exactamente $1$, y $\lambda = 1$ es un valor propio algebraicamente simple.
2. Todo otro valor propio $\mu$ de $P$ satisface el límite superior $|\mu| \le 1$.
3. Existe un único vector propio izquierdo normalizado $\pi = (\pi_1, \dots, \pi_N)$ asociado al valor propio $\lambda = 1$, tal que $\pi_i > 0$ para todo $i$ y $\sum_{i=1}^N \pi_i = 1$. (Esta es la distribución estacionaria única de la cadena).
4. Si, además, la cadena es aperiódica, entonces todo otro valor propio $\mu \\neq 1$ satisface estrictamente $|\mu| < 1$, lo que garantiza la convergencia geométrica $\lim_{n \\to \infty} P^n = \mathbf{1}\pi^T$.""")
        
        st.markdown("Como demostramos en el Ejercicio 2, nuestra matriz $P$ es irreducible, y al ser una matriz de probabilidad, satisface las hipótesis del Teorema de Perron-Frobenius. Planteamos el sistema de ecuaciones desarrollando el producto del vector fila $\pi$ por las columnas de $P$:")
        st.latex(rf"""
        \begin{{aligned}}
        \pi_1 &= {f2l(p1)}\pi_1 + 0\pi_2 + {f2l(p5)}\pi_3 \\
        \pi_2 &= {f2l(p2)}\pi_1 + {f2l(p3)}\pi_2 + 0\pi_3 \\
        \pi_3 &= 0\pi_1 + {f2l(p4)}\pi_2 + {f2l(p6)}\pi_3
        \end{{aligned}}
        """)
        st.markdown("Como los renglones de $P$ suman 1, el sistema es linealmente dependiente. Omitiremos la tercera ecuación y utilizaremos la ecuación de normalización: $\pi_1 + \pi_2 + \pi_3 = 1$. Despejamos $\pi_3$ y $\pi_2$ en términos de $\pi_1$:")
        st.latex(rf"""
        \begin{{aligned}}
        \pi_3 &= {f2l(k3)}\pi_1 \\
        \pi_2 &= {f2l(k2)}\pi_1
        \end{{aligned}}
        """)
        st.markdown("Sustituimos estas expresiones en la ecuación de normalización:")
        st.latex(rf"""
        \begin{{aligned}}
        \pi_1 + {f2l(k2)}\pi_1 + {f2l(k3)}\pi_1 &= 1 \\
        \pi_1 \left( 1 + {f2l(k2)} + {f2l(k3)} \right) &= 1 \\
        \pi_1 \left( {f2l(sum_k)} \right) &= 1 \implies \pi_1 = {f2l(pi1)}
        \end{{aligned}}
        """)
        st.markdown(f"Ahora que tenemos $\pi_1$, encontramos los demás valores sustituyendo hacia atrás obteniendo $\pi_2 = {f2l(pi2)}$ y $\pi_3 = {f2l(pi3)}$. La única distribución estacionaria es:")
        st.latex(rf"\pi = \left({f2l(pi1)},\ {f2l(pi2)},\ {f2l(pi3)}\right)")

        st.header("Ejercicio 5")
        st.markdown("**Pregunta:** Discuta el comportamiento de $P^n$ cuando $n\rightarrow\infty$. Interprete el resultado en términos probabilísticos.")
        st.info("**Teorema Límite / Teorema de Convergencia, Durrett, *Essentials of Stochastic Processes*, Teorema 1.19:** Supongamos que una cadena de Markov finita es irreducible y aperiódica, con distribución estacionaria $\pi$. Entonces, $\lim_{n \to \infty} P^n_{ij} = \pi_j$ para toda condición inicial $i$.")
        
        st.markdown(f"Para aplicar los teoremas de convergencia, primero analizamos la aperiodicidad de la cadena. El periodo $d(i)$ de un estado $i$ se define como el máximo común divisor de los instantes en los que el retorno es posible: $d(i) = \text{{mcd}}\\{{n \ge 1 : P^n(i,i) > 0\\}}$.\n\nObservamos que $P_{{11}} = {f2l(p1)} > 0$. Esto indica que el proceso puede regresar al estado 1 en exactamente 1 paso. Dado que $1 \in \\{{n \ge 1 : P^n_{{11}} > 0\\}}$, el mcd de este conjunto es por definición 1. Así, $d(1)=1$. Como la aperiodicidad es una propiedad de clase y la cadena es irreducible, todos los estados tienen periodo 1. La cadena es **aperiódica**.")
        
        st.markdown("El **Teorema Ergódico para Cadenas de Markov** establece que para una cadena irreducible, aperiódica y con distribución estacionaria $\pi$ (recurrente positiva), la probabilidad de transición converge a la probabilidad estacionaria, perdiendo memoria del estado inicial:")
        st.latex(rf"\lim_{{n\to\infty}} P^n = \mathbf{{1}}\pi^T = \begin{{pmatrix}} {f2l(pi1)} & {f2l(pi2)} & {f2l(pi3)} \\ {f2l(pi1)} & {f2l(pi2)} & {f2l(pi3)} \\ {f2l(pi1)} & {f2l(pi2)} & {f2l(pi3)} \end{{pmatrix}}")
        st.markdown("**Interpretación probabilística:** Cuando observamos el sistema a largo plazo ($n$ grande), la distribución de probabilidad de $X_n$ se estabiliza. Sin importar en qué estado ($X_0$) inició la cadena, la probabilidad incondicional de encontrar al sistema en el estado $j$ se aproximará asintóticamente a $\pi_j$. Además, por la Ley Fuerte de los Grandes Números para Cadenas de Markov, $\pi_j$ representa la fracción promedio de tiempo empírico que el proceso pasará en el estado $j$ a lo largo de una trayectoria infinita.")

        st.header("Ejercicio 6")
        st.markdown("**Pregunta:** Clasificación de estados y tiempos de absorción. Con base en la matriz P obtenida a partir de su número de cuenta, responda:\na) Clasifique cada estado (1, 2 y 3) como recurrente o transitorio. Justifique su respuesta.\nb) ¿Es la cadena aperiódica? Justifique.\nc) ¿Es la cadena ergódica? Justifique.\nd) Suponga que la cadena inicia en el estado 2. Defina $\tau = \min\{n\ge 0 : X_n \ne 2\}$ como el tiempo de salida del estado 2. Calcule el tiempo esperado $\mathbb{E}[\tau \mid X_0=2]$.\ne) Si la cadena comienza en el estado 1, calcule la probabilidad de que alguna vez alcance el estado 3.")
        
        st.markdown("**a) Recurrencia:** Un estado $i$ es recurrente si la probabilidad de retornar a él alguna vez, dado que inició en $i$, es 1. Es un teorema bien conocido que en un espacio de estados finito, no todos los estados pueden ser transitorios. Como nuestra cadena es **irreducible** (todos los estados pertenecen a la misma clase de comunicación), todos comparten la misma clasificación. Por ende, la existencia de al menos un estado recurrente obliga a que todos lo sean. Los estados 1, 2 y 3 son **recurrentes positivos**.")
        
        st.markdown("**b) Aperiodicidad:** Como se demostró en el Ejercicio 5, las transiciones de tipo auto-bucle ($P_{{ii}} > 0$) garantizan retornos en 1 paso, lo que hace que el máximo común divisor de los tiempos de retorno sea 1. Como la cadena es irreducible, la aperiodicidad se transfiere a toda la cadena. La cadena es **aperiódica**.")
        
        st.markdown("**c) Ergodicidad:** Por definición, una cadena se denomina **ergódica** si cumple tres condiciones: es irreducible, aperiódica y recurrente positiva. Ya hemos probado exhaustivamente que la cadena en cuestión cumple las tres propiedades. Por consiguiente, la cadena es **ergódica**.")

        st.markdown("**d) Tiempo esperado de salida del estado 2:**")
        st.markdown(f"Definimos la variable aleatoria $\\tau = \inf\\{{n\ge 0 : X_n \\neq 2\\}}$ que mide el número de pasos consecutivos que el proceso permanece en el estado 2 antes de transitar a un estado diferente.\nCondicionado a estar en el estado 2 ($X_0 = 2$), en cada iteración del reloj el sistema ejecuta un ensayo de Bernoulli:\n* \"Fracaso\" (permanecer en 2) con probabilidad $P_{{22}} = {f2l(p3)}$.\n* \"Éxito\" (salir de 2) con probabilidad $p = 1 - P_{{22}} = 1 - {f2l(p3)} = {f2l(p4)}$.\n\nDado que el proceso pierde memoria en cada paso (Propiedad de Markov), la cantidad de intentos necesarios para obtener el primer \"éxito\" sigue una distribución Geométrica con parámetro $p = {f2l(p4)}$. El valor esperado de una variable geométrica (contando el intento final de salida) está dado por $1/p$. Por lo tanto:")
        st.latex(rf"\mathbb{{E}}_2[\tau] = \frac{{1}}{{p}} = \frac{{1}}{{{f2l(p4)}}} = {f2l(e_tau)} = {float(e_tau):.2f} \text{{ pasos}}.")

        st.markdown("**e) Probabilidad de alcanzar el estado 3 desde el estado 1:**")
        st.markdown(r"Sea $h_i = \mathbb{P}( \tau_3 < \infty \mid X_0 = i)$ la probabilidad de alguna vez alcanzar el estado 3 habiendo iniciado en $i$, donde $\tau_3 = \inf\{n \ge 0 : X_n = 3\}$. Por definición, si iniciamos en 3, ya estamos ahí, así que $h_3 = 1$. Para los demás estados, planteamos el sistema de ecuaciones lineales condicionales (análisis del primer paso), basado en la ley de probabilidad total:")
        st.latex(rf"""
        \begin{{aligned}}
        h_1 &= {f2l(p1)}h_1 + {f2l(p2)}h_2 + 0 \\
        h_2 &= 0 + {f2l(p3)}h_2 + {f2l(p4)}(1)
        \end{{aligned}}
        """)
        
        st.markdown("Resolvemos la segunda ecuación rigurosamente:")
        st.latex(rf"""
        \begin{{aligned}}
        h_2 - {f2l(p3)}h_2 &= {f2l(p4)} \\
        {f2l(p4)}h_2 &= {f2l(p4)} \implies h_2 = 1
        \end{{aligned}}
        """)
        
        st.markdown("Sustituimos $h_2 = 1$ en la primera ecuación:")
        st.latex(rf"""
        \begin{{aligned}}
        h_1 - {f2l(p1)}h_1 &= {f2l(p2)}(1) \\
        {f2l(p2)}h_1 &= {f2l(p2)} \implies h_1 = 1
        \end{{aligned}}
        """)
        
        st.markdown("La solución matemática al sistema armónico confirma que la probabilidad $\mathbb{P}_1(\tau_3 < \infty) = 1$. Esto concuerda con el resultado teórico esperado: dado que la cadena es irreducible y recurrente positiva, cualquier estado visita eventualmente a todos los demás con probabilidad 1 (casi seguramente).")

        st.divider()

        # ==========================================
        # 3. GENERACIÓN DEL TEMPLATE LATEX EXACTO
        # ==========================================
        latex_template = r"""\documentclass[12pt, letterpaper]{article}
\usepackage[utf8]{inputenc}
\usepackage[spanish, es-tabla]{babel}
\usepackage{amsmath, amsthm, amssymb, mathrsfs}
\usepackage{geometry}
\geometry{top=2.5cm, bottom=2.5cm, left=2.5cm, right=2.5cm}

% Librerías para el grafo
\usepackage{tikz}
\usetikzlibrary{automata, positioning, arrows.meta, babel}

% Entornos formales
\newtheorem{theorem}{Teorema}
\newtheorem{definition}{Definición}
\newtheorem{lemma}{Lema}
\newtheorem{proposition}{Proposición}

\title{\textbf{Examen Procesos Estocásticos - Parcial I}}
\author{ \\  __CUENTA__\textbf{Número de cuenta:} __CUENTA__}
\date{}

\begin{document}

\maketitle

\section*{Definición Preliminar del Espacio de Probabilidad}

Sea $(\Omega, \mathcal{F}, \mathbb{P})$ un espacio de probabilidad y $I = \{1, 2, 3\}$ un espacio de estados finito dotado de la $\sigma$-álgebra discreta $\mathcal{P}(I)$. Definimos el proceso estocástico $X = (X_n)_{n \in \mathbb{N}_0}$ adaptado a su filtración natural $\mathcal{F}_n = \sigma(X_0, \dots, X_n)$.

Evaluando los escalares del número de cuenta proporcionado: $a_1=__A1__, a_2=__A2__, a_3=__A3__, a_4=__A4__, a_5=__A5__, a_6=__A6__$.

\vspace{0.5cm}
\hrule
\vspace{0.5cm}

\section*{Ejercicio 1}
\textbf{Pregunta:} Considere la matriz que acaba de construir.
a) Demuestre que $p_1+p_2=1$, $p_3+p_4=1$, $p_5+p_6=1$. Deduzca que la matriz P es estocástica. Calcule explícitamente P usando su número de cuenta.

\vspace{0.3cm}
\textbf{Solución:}
\begin{definition}[Matriz Estocástica]
Una matriz $P = (p_{ij})_{i,j \in I}$ se denomina matriz estocástica (o matriz de transición de Markov) si satisface:
1. $p_{ij} \ge 0$ para todo $i, j \in I$.
2. $\sum_{j \in I} p_{ij} = 1$ para todo $i \in I$.
\end{definition}
Procedemos a sustituir los valores de los escalares $a_k$ en las fórmulas para los coeficientes del núcleo de transición de Markov $K: I \times \mathcal{P}(I) \to [0,1]$. Realizamos el cálculo paso a paso:

Para la primera fila (desde el estado 1):
\begin{align*}
p_1 &= \frac{a_1+1}{a_1+a_2+2} = \frac{__A1__+1}{__A1__+__A2__+2} = __P1__, \\[4pt]
p_2 &= \frac{a_2+1}{a_1+a_2+2} = \frac{__A2__+1}{__A1__+__A2__+2} = __P2__.
\end{align*}

Para la segunda fila (desde el estado 2):
\begin{align*}
p_3 &= \frac{a_3+1}{a_3+a_4+2} = \frac{__A3__+1}{__A3__+__A4__+2} = __P3__, \\[4pt]
p_4 &= \frac{a_4+1}{a_3+a_4+2} = \frac{__A4__+1}{__A3__+__A4__+2} = __P4__.
\end{align*}

Para la tercera fila (desde el estado 3):
\begin{align*}
p_5 &= \frac{a_5+1}{a_5+a_6+2} = \frac{__A5__+1}{__A5__+__A6__+2} = __P5__, \\[4pt]
p_6 &= \frac{a_6+1}{a_5+a_6+2} = \frac{__A6__+1}{__A5__+__A6__+2} = __P6__.
\end{align*}

Para demostrar que $P$ es una matriz estocástica, debemos comprobar que la suma de las probabilidades de transición desde cualquier estado $i$ hacia todos los estados $j \in I$ es exactamente igual a 1. Es decir, $\sum_{j\in I}P(i,j)=1$:

\begin{itemize}
    \item \textbf{Fila 1:} $p_1+p_2 = __P1__ + __P2__ = 1$.
    \item \textbf{Fila 2:} $p_3+p_4 = __P3__ + __P4__ = 1$.
    \item \textbf{Fila 3:} $p_5+p_6 = __P5__ + __P6__ = 1$.
\end{itemize}

Como todas las entradas son no negativas ($P(i,j) \ge 0$) y las sumas por fila son 1, deducimos formalmente que $P$ es una matriz estocástica. Construyendo la matriz con estos coeficientes y rellenando con ceros las transiciones no definidas, obtenemos:
\[
P = \begin{pmatrix} __P1__ & __P2__ & 0 \\[4pt] 0 & __P3__ & __P4__ \\[4pt] __P5__ & 0 & __P6__ \end{pmatrix}.
\]

\vspace{0.5cm}
\hrule
\vspace{0.5cm}

\section*{Ejercicio 2}
\textbf{Pregunta:} Considere la cadena de Markov con matriz de transición P.
a) Dibuje el grafo de transición.
b) Determine las clases de comunicación.
c) Estudie si la cadena es irreducible.

\vspace{0.3cm}
\textbf{Solución:}

\textbf{a) Grafo de transición:} 
El soporte del núcleo de transición nos indica las aristas del grafo dirigido $G = (I, E)$. Existe una arista dirigida de $i$ a $j$ si y solo si $P(i,j) > 0$.
\begin{center}
\begin{tikzpicture}[->, >={Stealth[round]}, shorten >=1pt, auto, node distance=3.5cm, semithick]
    \node[state] (1) {1};
    \node[state] (2) [right of=1] {2};
    \node[state] (3) [below right of=1] {3};

    \path
        (1) edge [loop left] node {$__P1__$} (1)
            edge node {$__P2__$} (2)
        (2) edge [loop right] node {$__P3__$} (2)
            edge node {$__P4__$} (3)
        (3) edge [bend left] node {$__P5__$} (1)
            edge [loop below] node {$__P6__$} (3);
\end{tikzpicture}
\end{center}

\textbf{b) y c) Clases de comunicación e Irreducibilidad:}
\begin{definition}
Decimos que el estado $j$ es accesible desde $i$ ($i \to j$) si existe un $n \ge 0$ tal que $P^n(i,j) > 0$. Dos estados se comunican ($i \leftrightarrow j$) si $i \to j$ y $j \to i$. Una cadena de Markov es \textbf{irreducible} si todos sus estados pertenecen a una única clase de comunicación.
\end{definition}

A partir de las probabilidades de transición en un paso ($n=1$), observamos las siguientes rutas directas:
\begin{itemize}
    \item $1 \to 2$ (pues $P_{12} = __P2__ > 0$)
    \item $2 \to 3$ (pues $P_{23} = __P4__ > 0$)
    \item $3 \to 1$ (pues $P_{31} = __P5__ > 0$)
\end{itemize}

Dado que podemos establecer el ciclo $1 \to 2 \to 3 \to 1$, podemos transitar de cualquier estado a cualquier otro en un número finito de pasos. Por ejemplo, para ir de 1 a 3, usamos la ruta $1 \to 2 \to 3$ en $n=2$ pasos, asegurando que $P^2_{13} > 0$. 

Dado que el grafo dirigido asociado es fuertemente conexo, todos los estados se comunican entre sí. Concluimos que la cadena es \textbf{irreducible} y posee una única clase de comunicación: $C=\{1,2,3\}$.

\vspace{0.5cm}
\hrule
\vspace{0.5cm}

\section*{Ejercicio 3}
\textbf{Pregunta:} Calcule la matriz $P^2$ e interprete probabilísticamente las entradas de $P^2$. Además, determine $\mathbb{P}(X_2=3|X_0=1)$.

\vspace{0.3cm}
\textbf{Solución:}
\begin{theorem}[Ecuaciones de Chapman-Kolmogorov]
Para cualesquiera estados $i, j$ y tiempos $n, m \ge 0$, la probabilidad de transición a $n+m$ pasos satisface:
$P^{n+m}_{ij} = \sum_{k \in I} P^n_{ik} P^m_{kj}$. En notación matricial, $P^{n+m} = P^n P^m$.
\end{theorem}

Tomemos el teorema de Ecuaciones de Chapman-Kolmogorov $P^{n+m} = P^nP^m$. Para hallar las probabilidades a dos pasos, debemos calcular $P^2 = P \times P$ mediante la convolución discreta (multiplicación fila por columna).

Entonces con eso desarrollamos el producto algebraico explícitamente:
\[
P^2 = 
\begin{pmatrix} __P1__ & __P2__ & 0 \\[4pt] 0 & __P3__ & __P4__ \\[4pt] __P5__ & 0 & __P6__ \end{pmatrix}
\begin{pmatrix} __P1__ & __P2__ & 0 \\[4pt] 0 & __P3__ & __P4__ \\[4pt] __P5__ & 0 & __P6__ \end{pmatrix}
\]

Cálculo de las entradas de $P^2$:
\begin{itemize}
    \item \textbf{Fila 1:}
    \begin{align*}
    (P^2)_{11} &= \left(__P1__\right)\left(__P1__\right) + \left(__P2__\right)(0) + (0)\left(__P5__\right) = __P2_11__ \\
    (P^2)_{12} &= \left(__P1__\right)\left(__P2__\right) + \left(__P2__\right)\left(__P3__\right) + (0)(0) = __P2_12__ \\
    (P^2)_{13} &= \left(__P1__\right)(0) + \left(__P2__\right)\left(__P4__\right) + (0)\left(__P6__\right) = __P2_13__
    \end{align*}
    
    \item \textbf{Fila 2:}
    \begin{align*}
    (P^2)_{21} &= (0)\left(__P1__\right) + \left(__P3__\right)(0) + \left(__P4__\right)\left(__P5__\right) = __P2_21__ \\
    (P^2)_{22} &= (0)\left(__P2__\right) + \left(__P3__\right)\left(__P3__\right) + \left(__P4__\right)(0) = __P2_22__ \\
    (P^2)_{23} &= (0)(0) + \left(__P3__\right)\left(__P4__\right) + \left(__P4__\right)\left(__P6__\right) = __P2_23__
    \end{align*}
    
    \item \textbf{Fila 3:}
    \begin{align*}
    (P^2)_{31} &= \left(__P5__\right)\left(__P1__\right) + (0)(0) + \left(__P6__\right)\left(__P5__\right) = __P2_31__ \\
    (P^2)_{32} &= \left(__P5__\right)\left(__P2__\right) + (0)\left(__P3__\right) + \left(__P6__\right)(0) = __P2_32__ \\
    (P^2)_{33} &= \left(__P5__\right)(0) + (0)\left(__P4__\right) + \left(__P6__\right)\left(__P6__\right) = __P2_33__
    \end{align*}
\end{itemize}

Por lo tanto, la matriz a dos pasos es:
\[
P^2 = 
\begin{pmatrix} __P2_11__ & __P2_12__ & __P2_13__ \\[6pt] __P2_21__ & __P2_22__ & __P2_23__ \\[6pt] __P2_31__ & __P2_32__ & __P2_33__ \end{pmatrix}.
\]

\textbf{Interpretación probabilística:} Cada entrada $(P^2)_{ij}$ representa la suma de las probabilidades de todas las trayectorias posibles de longitud exacta $n=2$ que comienzan en el estado $i$ y terminan en el estado $j$. Es decir, es la probabilidad de transición condicional $\mathbb{P}(X_2 = j \mid X_0 = i)$.

Para el caso particular solicitado:
\[
\mathbb{P}(X_2 = 3 \mid X_0 = 1) = (P^2)_{13} = __P2_13__ \approx __P2_13_DEC__.
\]
Notemos que la única ruta posible en 2 pasos para ir de 1 a 3 es la trayectoria $1 \to 2 \to 3$, cuya probabilidad es exactamente $P_{12} \times P_{23} = (__P2__) \times (__P4__) = __P2_13__$.

\vspace{0.5cm}
\hrule
\vspace{0.5cm}

\section*{Ejercicio 4}
\textbf{Pregunta:} Sea $\pi=(\pi_1,\pi_2,\pi_3)$. Resuelva $\pi P = \pi$ con la condición $\pi_1+\pi_2+\pi_3=1$. Obtenga la distribución estacionaria correspondiente a su número de cuenta.

\vspace{0.3cm}
\begin{theorem}[Teorema de Perron-Frobenius para Matrices Estocásticas]
Sea $P$ una matriz estocástica de dimensión $N \times N$ correspondiente a una cadena de Markov finita e irreducible. Entonces:
\begin{enumerate}
    \item El radio espectral de $P$ es exactamente $1$, y $\lambda = 1$ es un valor propio algebraicamente simple.
    \item Todo otro valor propio $\mu$ de $P$ satisface el límite superior $|\mu| \le 1$.
    \item Existe un único vector propio izquierdo normalizado $\pi = (\pi_1, \dots, \pi_N)$ asociado al valor propio $\lambda = 1$, tal que $\pi_i > 0$ para todo $i$ y $\sum_{i=1}^N \pi_i = 1$. (Esta es la distribución estacionaria única de la cadena).
    \item Si, además, la cadena es aperiódica (lo que equivale a que la matriz $P$ sea \textit{primitiva}, es decir, existe un entero $m \ge 1$ tal que todas las entradas de $P^m$ son estrictamente positivas), entonces todo otro valor propio $\mu \neq 1$ satisface estrictamente $|\mu| < 1$, lo que garantiza la convergencia geométrica $\lim_{n \to \infty} P^n = \mathbf{1}\pi^T$.
\end{enumerate}
\end{theorem}

\vspace{0.3cm}
Como demostramos en el Ejercicio 2, nuestra matriz $P$ es irreducible, y al ser una matriz de probabilidad, satisface las hipótesis del Teorema de Perron-Frobenius. Por lo tanto, el sistema $\pi P = \pi$ (que corresponde a encontrar el vector propio izquierdo asociado a $\lambda=1$) tiene una solución estrictamente positiva y única bajo la condición de normalización $\sum \pi_i = 1$.

Planteamos el sistema de ecuaciones desarrollando el producto del vector fila $\pi$ por las columnas de $P$:
\begin{align}
\pi_1 &= __P1__\pi_1 + 0\pi_2 + __P5__\pi_3 \label{eq1} \\
\pi_2 &= __P2__\pi_1 + __P3__\pi_2 + 0\pi_3 \label{eq2} \\
\pi_3 &= 0\pi_1 + __P4__\pi_2 + __P6__\pi_3 \label{eq3}
\end{align}

Como los renglones de $P$ suman 1, el sistema es linealmente dependiente. Omitiremos la ecuación (\ref{eq3}) y utilizaremos la ecuación de normalización: $\pi_1 + \pi_2 + \pi_3 = 1$.

Despejamos $\pi_3$ en términos de $\pi_1$ a partir de (\ref{eq1}):
\begin{align*}
\pi_1 - __P1__\pi_1 &= __P5__\pi_3 \\
\pi_3 &= __K3__\pi_1
\end{align*}

Despejamos $\pi_2$ en términos de $\pi_1$ a partir de (\ref{eq2}):
\begin{align*}
\pi_2 - __P3__\pi_2 &= __P2__\pi_1 \\
\pi_2 &= __K2__\pi_1
\end{align*}

Sustituimos estas expresiones en la ecuación de normalización:
\begin{align*}
\pi_1 + \pi_2 + \pi_3 &= 1 \\
\pi_1 + __K2__\pi_1 + __K3__\pi_1 &= 1 \\
\pi_1 \left( 1 + __K2__ + __K3__ \right) &= 1 \\
\pi_1 \left( __SUM_K__ \right) &= 1 \implies \pi_1 = __PI1__
\end{align*}

Ahora que tenemos $\pi_1$, encontramos los demás valores sustituyendo hacia atrás:
\begin{align*}
\pi_2 &= __K2__ \left( __PI1__ \right) = __PI2__ \\[4pt]
\pi_3 &= __K3__ \left( __PI1__ \right) = __PI3__
\end{align*}

Para verificar la consistencia matemática, comprobamos que se satisfaga la ecuación (\ref{eq3}) que habíamos omitido:
\[
__P4__\pi_2 + __P6__\pi_3 = __P4__\left(__PI2__\right) + __P6__\left(__PI3__\right) = __PI3__ = \pi_3.
\]
La verificación es correcta. Por lo tanto, la única distribución estacionaria es:
\[
\pi = \left(__PI1__,\ __PI2__,\ __PI3__\right).
\]

\vspace{0.5cm}
\hrule
\vspace{0.5cm}

\section*{Ejercicio 5}
\textbf{Pregunta:} Discuta el comportamiento de $P^n$ cuando $n\rightarrow\infty$. Interprete el resultado en términos probabilísticos.

\vspace{0.3cm}
\textbf{Solución:}
\begin{theorem}[Teorema Límite / Teorema de Convergencia, Durrett, \textit{Essentials of Stochastic Processes}, Teorema 1.19]
Supongamos que una cadena de Markov finita es irreducible y aperiódica, con distribución estacionaria $\pi$. Entonces, $\lim_{n \to \infty} P^n_{ij} = \pi_j$ para toda condición inicial $i$.
\end{theorem}
Para aplicar los teoremas de convergencia, primero analizamos la aperiodicidad de la cadena. El periodo $d(i)$ de un estado $i$ se define como el máximo común divisor de los instantes en los que el retorno es posible: $d(i) = \text{mcd}\{n \ge 1 : P^n(i,i) > 0\}$.

Observamos que $P_{11} = __P1__ > 0$. Esto indica que el proceso puede regresar al estado 1 en exactamente 1 paso. Dado que $1 \in \{n \ge 1 : P^n_{11} > 0\}$, el mcd de este conjunto es por definición 1. Así, $d(1)=1$. Como la aperiodicidad es una propiedad de clase y la cadena es irreducible, todos los estados tienen periodo 1. La cadena es \textbf{aperiódica}.

El \textbf{Teorema Ergódico para Cadenas de Markov} establece que para una cadena irreducible, aperiódica y con distribución estacionaria $\pi$ (recurrente positiva), la probabilidad de transición $n$-pasos converge a la probabilidad estacionaria, perdiendo memoria del estado inicial:
\[
\lim_{n\to\infty} P^n_{ij} = \pi_j \quad \text{para todo } i,j\in I.
\]

Matricialmente, esto significa que cuando $n \to \infty$, $P^n$ converge a una matriz cuyas filas son todas idénticas al vector invariante $\pi$:
\[
\lim_{n\to\infty} P^n = \mathbf{1}\,\pi^T =
\begin{pmatrix}
__PI1__ & __PI2__ & __PI3__\\[4pt]
__PI1__ & __PI2__ & __PI3__\\[4pt]
__PI1__ & __PI2__ & __PI3__
\end{pmatrix}.
\]

\textbf{Interpretación probabilística:} 
Cuando observamos el sistema a largo plazo ($n$ grande), la distribución de probabilidad de $X_n$ se estabiliza. Sin importar en qué estado ($X_0$) inició la cadena, la probabilidad incondicional de encontrar al sistema en el estado $j$ se aproximará asintóticamente a $\pi_j$. Además, por la Ley Fuerte de los Grandes Números para Cadenas de Markov, $\pi_j$ representa la fracción promedio de tiempo empírico que el proceso pasará en el estado $j$ a lo largo de una trayectoria infinita.

\vspace{0.5cm}
\hrule
\vspace{0.5cm}

\section*{Ejercicio 6}
\textbf{Pregunta:} Clasificación de estados y tiempos de absorción. Con base en la matriz P obtenida a partir de su número de cuenta, responda:
a) Clasifique cada estado (1, 2 y 3) como recurrente o transitorio. Justifique su respuesta.
b) ¿Es la cadena aperiódica? Justifique.
c) ¿Es la cadena ergódica? Justifique.
d) Suponga que la cadena inicia en el estado 2. Defina $\tau = \min\{n\ge 0 : X_n \ne 2\}$ como el tiempo de salida del estado 2. Calcule el tiempo esperado $\mathbb{E}[\tau \mid X_0=2]$.
e) Si la cadena comienza en el estado 1, calcule la probabilidad de que alguna vez alcance el estado 3.

\vspace{0.3cm}
\textbf{Solución:}

\textbf{a) Recurrencia:} Un estado $i$ es recurrente si la probabilidad de retornar a él alguna vez, dado que inició en $i$, es 1 (es decir, $f_{ii} = 1$). Es un teorema bien conocido que en un espacio de estados finito, no todos los estados pueden ser transitorios. Como nuestra cadena es \textbf{irreducible} (todos los estados pertenecen a la misma clase de comunicación), todos comparten la misma clasificación. Por ende, la existencia de al menos un estado recurrente obliga a que todos lo sean. Los estados 1, 2 y 3 son \textbf{recurrentes positivos}.

\textbf{b) Aperiodicidad:} Como se demostró en el Ejercicio 5, las transiciones de tipo auto-bucle ($P_{ii} > 0$) garantizan retornos en 1 paso, lo que hace que el máximo común divisor de los tiempos de retorno sea 1. Como la cadena es irreducible, la aperiodicidad se transfiere a toda la cadena. La cadena es \textbf{aperiódica}.

\textbf{c) Ergodicidad:} Por definición, una cadena se denomina \textbf{ergódica} si cumple tres condiciones: es irreducible, aperiódica y recurrente positiva. Ya hemos probado exhaustivamente que la cadena en cuestión cumple las tres propiedades. Por consiguiente, la cadena es \textbf{ergódica}.

\textbf{d) Tiempo esperado de salida del estado 2:}
Definimos la variable aleatoria $\tau = \inf\{n\ge 0 : X_n \neq 2\}$ que mide el número de pasos consecutivos que el proceso permanece en el estado 2 antes de transitar a un estado diferente.
Condicionado a estar en el estado 2 ($X_0 = 2$), en cada iteración del reloj el sistema ejecuta un ensayo de Bernoulli:
\begin{itemize}
    \item "Fracaso" (permanecer en 2) con probabilidad $P_{22} = __P3__$.
    \item "Éxito" (salir de 2) con probabilidad $p = 1 - P_{22} = 1 - __P3__ = __P4__$.
\end{itemize}
Dado que el proceso pierde memoria en cada paso (Propiedad de Markov), la cantidad de intentos necesarios para obtener el primer "éxito" sigue una distribución Geométrica con parámetro $p = __P4__$.
El valor esperado de una variable geométrica (contando el intento final de salida) está dado por $1/p$. Por lo tanto:
\[
\mathbb{E}_2[\tau] = \frac{1}{p} = \frac{1}{__P4__} = __ETAU__ = __ETAU_DEC__ \text{ pasos}.
\]

\textbf{e) Probabilidad de alcanzar el estado 3 desde el estado 1:}
Sea $h_i = \mathbb{P}( \tau_3 < \infty \mid X_0 = i)$ la probabilidad de alguna vez alcanzar el estado 3 habiendo iniciado en $i$, donde $\tau_3 = \inf\{n \ge 0 : X_n = 3\}$.
Por definición, si iniciamos en 3, ya estamos ahí, así que $h_3 = 1$.
Para los demás estados, planteamos el sistema de ecuaciones lineales condicionales (análisis del primer paso), basado en la ley de probabilidad total:
\begin{align*}
h_1 &= P_{11}h_1 + P_{12}h_2 + P_{13}h_3 \\
h_2 &= P_{21}h_1 + P_{22}h_2 + P_{23}h_3
\end{align*}

Sustituyendo las probabilidades de nuestra matriz $P$:
\begin{align}
h_1 &= __P1__h_1 + __P2__h_2 + 0 \label{h1} \\
h_2 &= 0 + __P3__h_2 + __P4__(1) \label{h2}
\end{align}

Resolvemos la ecuación (\ref{h2}) rigurosamente:
\begin{align*}
h_2 - __P3__h_2 &= __P4__ \\
__P4__h_2 &= __P4__ \implies h_2 = 1
\end{align*}

Sustituimos $h_2 = 1$ en la ecuación (\ref{h1}):
\begin{align*}
h_1 - __P1__h_1 &= __P2__(1) \\
__P2__h_1 &= __P2__ \implies h_1 = 1
\end{align*}

La solución matemática al sistema armónico confirma que la probabilidad $\mathbb{P}_1(\tau_3 < \infty) = 1$. Esto concuerda con el resultado teórico esperado: dado que la cadena es irreducible y recurrente positiva, cualquier estado visita eventualmente a todos los demás con probabilidad 1 (casi seguramente).

\end{document}
"""

        # Motor de reemplazos
        reemplazos = {
            "__CUENTA__": cuenta,
            "__A1__": str(a1), "__A2__": str(a2), "__A3__": str(a3),
            "__A4__": str(a4), "__A5__": str(a5), "__A6__": str(a6),
            
            "__P1__": f2l(p1), "__P2__": f2l(p2), "__P3__": f2l(p3),
            "__P4__": f2l(p4), "__P5__": f2l(p5), "__P6__": f2l(p6),
            
            "__P2_11__": f2l(p2_11), "__P2_12__": f2l(p2_12), "__P2_13__": f2l(p2_13),
            "__P2_21__": f2l(p2_21), "__P2_22__": f2l(p2_22), "__P2_23__": f2l(p2_23),
            "__P2_31__": f2l(p2_31), "__P2_32__": f2l(p2_32), "__P2_33__": f2l(p2_33),
            "__P2_13_DEC__": f"{float(p2_13):.4f}",
            
            "__K2__": f2l(k2), "__K3__": f2l(k3), "__SUM_K__": f2l(sum_k),
            "__PI1__": f2l(pi1), "__PI2__": f2l(pi2), "__PI3__": f2l(pi3),
            
            "__ETAU__": f2l(e_tau), "__ETAU_DEC__": f"{float(e_tau):.2f}"
        }

        documento_final = latex_template
        for clave, valor in reemplazos.items():
            documento_final = documento_final.replace(clave, valor)

        st.subheader("Descarga y Código LaTeX")
        st.markdown("Si deseas compilar esto en tu editor local, descarga el archivo aquí o copia el código directamente del bloque inferior:")
        
        st.download_button(
            label=" Descargar archivo .tex",
            data=documento_final,
            file_name=f"Examen_{cuenta}.tex",
            mime="text/plain"
        )
        
        with st.expander("Ver el código LaTeX generado", expanded=False):
            st.code(documento_final, language="latex")
            
    else:
        st.error(" El número de cuenta debe tener al menos 6 dígitos numéricos.")