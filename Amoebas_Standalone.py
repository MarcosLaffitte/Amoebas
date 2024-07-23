################################################################################
#                                                                              #
#  README - Programa: Amoebas_Standalone.py                                    #
#                                                                              #
#  - Hecho por: Mtr. Marcos Emmanuel Gonzalez Laffitte                         #
#  - Github: @MarcosLaffitte                                                   #
#  - Repositiorio:  https://github.com/MarcosLaffitte/Amoebas                  #
#  - Universidad Nacional Autonoma de Mexico (UNAM)                            #
#  - Instituto de Matematicas (IMATE), Unidad Juriquilla                       #
#  - Maestria en Ciencias Matematicas                                          #
#  - Tutoras: Dra. Amanda Montejano Cantoral y Dra. Adriana Hansberg Pastor    #
#  - Parte del trabajo de Tesis de @MarcosLaffitte:                            #
#                                                                              #
#                 "Estudio de Amoebas y sus Propiedades:                       #
#            Deteccion Computacional de esta Familia de Graficas               #
#                    y el Caso de los Reemplazos Raros"                        #
#                                                                              #
#  - Tesis UNAM: http://132.248.9.195/ptd2022/septiembre/0831065/Index.html    #
#  - Descripcion: recibe una graficas en codigo y determina si esta es amoeba  #
#    local y/o global, o bien si no es amoeba.                                 #
#                                                                              #
#  - Ejecutar como:                                                            #
#                      python  Amoebas_Standalone.py                           #
#                                                                              #
#  - Fecha: 23 de july 2024                                                    #
#                                                                              #
################################################################################


# Requiere #####################################################################


"""
> Lenguaje: python 3.7
> Anaconda: 4-bit version - conda 4.10.1
> Paquetes:  (instalados con anaconda)
***** networkx 2.5
***** sympy 1.7.1
***** matplotlib 3.3.3
"""


# Dependencias #################################################################


# instaladas con conda ---------------------------------------------------------
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.backends.backend_pdf
from networkx.algorithms import isomorphism
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics.perm_groups import PermutationGroup


# incluidas en python ----------------------------------------------------------
import time
import pickle
from sys import argv
from copy import deepcopy
from math import factorial, modf


# apagar warnings generales y de matplotlib ------------------------------------
import warnings
matplotlib.use("Agg")
warnings.filterwarnings("ignore")


# Variables ####################################################################


# datos ------------------------------------------------------------------------
orden = 0           # cantidad de vertices
tamano = 0          # cantidad de aristas
familia = ""        # solo "LA", solo "GA", "LAnGA", no amoeba "NO"


# factor de percepcion para imprimir avance ------------------------------------
factor = 0.025   # factor en segundos para evitar "flashasos" de barra de avance


# Funciones ####################################################################


# funcion: imprimir mensaje de avance ------------------------------------------
def imprimirAvance(num, tot, porcetajeCaso):
    # variables locales
    tail = "".join(10*[" "])
    base = "-"
    term = "="
    pila = []
    terminado = ""
    porcetajeInt = 0
    # parte 1
    parte1 = "* Analyzing graph " + str(num) + "/" + str(tot) + ";  "
    # parte 2
    porcetajeInt = int(modf(porcetajeCaso/10)[1])
    for i in range(1, 11):
        if(i <= porcetajeInt):
            pila.append(term)
        else:
            pila.append(base)
    terminado = "".join(pila)
    parte2 = "Progress on graph:  0%  [" + terminado + "]  100%"
    # mensaje
    print(parte1 + parte2 + tail, end = "\r")
    # fin de funcion


# funcion: pasar isomofismo diccionario a permutacion en lista -----------------
def isoListVersion(isoDict):
    # funcion basada en el trabajo del Dr. Rafael Villarroel Flores (sinodal de tesis)
    # variables locales
    i = 0
    isoList = []
    # convertir isomorfismo a lista [f(0), f(1), ..., f(n-1)]
    for i in range(len(isoDict)):
        isoList.append(isoDict[i])
    # fin de funcion
    return(isoList)


# funcion: isomorfismos de G en H como permutaciones de vertices ---------------
def obtenerIsomorfismos(someG, someH):
    # variables locales
    matcher = None
    isomorfismos = []
    isosComoPermutaciones = []
    iso = None
    # calcular isomorfismos con VF2
    matcher = isomorphism.GraphMatcher(someG, someH)  # deben tener los mismos vertices
    isomorfismos = list(matcher.isomorphisms_iter())
    # convertir isomorfismos a permutaciones en notacion ciclica
    isosComoPermutaciones = [Permutation(isoListVersion(iso)) for iso in isomorfismos]
    # fin de funcion
    return(isosComoPermutaciones)


# funcion: aplicar reemplazo de aristas a G ------------------------------------
def aplicarReemplazo(someG, vr, vs, vk, vl):
    # variables locales
    nuevaGrafica = None
    # realizar reemplazo
    nuevaGrafica = deepcopy(someG)
    nuevaGrafica.remove_edge(vr, vs)
    nuevaGrafica.add_edge(vk, vl)
    # fin de funcion
    return(nuevaGrafica)


# funcion: revisar las condiciones sobre los grados ----------------------------
def revisarCondicionesDeGrados(someG, vr, vs, vk, vl):
    # variables locales
    condicion = False
    dr = 0
    ds = 0
    dk = 0
    dl = 0
    gradosOriginal = []     # {d(vr), d(vs)}
    gradosNuevos = []       # {d(vk) + 1, d(vl) + 1}
    conservado = 0
    va = 0
    vb = 0
    da = 0
    db = 0
    # obtener los grados de vr, vs, vk, vl
    dr = someG.degree(vr)
    ds = someG.degree(vs)
    dk = someG.degree(vk)
    dl = someG.degree(vl)
    # obtener conjuntos de grados de vertices en el reemplazo (no trivial)
    gradosOriginal = [dr, ds]
    gradosOriginal.sort()
    gradosNuevos = [dk + 1, dl + 1]
    gradosNuevos.sort()
    # analizar caso  i)  |{r, s} n {k, l}| = 0
    if(len({vr, vs}.intersection({vk, vl})) == 0):
        # si {d(vk) + 1, d(vl) + 1} = {d(vr), d(vs)}, se mantienen las condiciones de grados
        if(gradosOriginal == gradosNuevos):
            condicion = True
    # analizar caso  ii) |{r, s} n {k, l}| = 1
    if(len({vr, vs}.intersection({vk, vl})) == 1):
        conservado = list({vr, vs}.intersection({vk, vl}))[0]
        va = list({vr, vs}.difference({conservado}))[0]
        vb = list({vk, vl}.difference({conservado}))[0]
        da = someG.degree(va)
        db = someG.degree(vb)
        # si d(vb) + 1 = d(va), se mantienen las condiciones de grados
        if(db + 1 == da):
            condicion = True
    # fin de funcion
    return(condicion)


# funcion: deteccion de amoebas entre graficas arbitrarias - no vacias!!! ------
def analizarAmoebasGraficasArbitrarias(G, numG, totalGraficas):
    # variables globales
    global factor
    # variables locales
    esLA = False
    esGA = False
    aristasG = []
    GuK1 = None
    compGuK1 = None
    compAristas = []
    n = 0                          # orden de G
    nMasUno = 0                    # orden de GuK1
    permutacionesLocales = []      # asociadas a reemplazos admisibles de G
    permutacionesGlobales = []     # asociadas a reemplazos admisibles de GuK1
    grupoGeneradoLocal = None      # grupo S_G
    grupoGeneradoGlobal = None     # grupo S_GuK1
    r = 0
    s = 0
    k = 0
    l = 0
    condicionesGrados = False
    graficaConReemplazo = None
    sonIsomorfas = False
    grados = []
    gradMin = 0
    gradMax = 0
    gradosTot = 0
    gradosCompletos = False
    familiaG = ""
    avance = 0
    porcentaje = 0
    tiempoInicial = 0
    tiempoFinal = 0
    ############################## ETAPA 1 ##############################
    # analizar conjunto de grados
    grados = list(set([d for (v, d) in list(G.degree())]))
    gradMin = min(grados)
    gradMax = max(grados)
    gradosTot = len(grados)
    if(not (gradosTot == (gradMax - (gradMin - 1)))):
        return("NO")
    # obtener "nombre" de nuevo vertice aislado; los demas se llaman 0, 1, ..., n-1 por default
    n = G.order()
    # hacer copia de la grafica original, agregar nuevo vertice aislado y obtener n+1 para evaluar (n+1)!
    GuK1 = deepcopy(G)
    GuK1.add_node(n)
    nMasUno = GuK1.order()
    # calcular automorfismos de G; permutaciones locales asociadas a todo reemplazo trivial
    permutacionesLocales = permutacionesLocales + obtenerIsomorfismos(G, G)
    # calcular automorfismos de GuK1; permutaciones globales asociadas a todo reemplazo trivial
    permutacionesGlobales = permutacionesGlobales + obtenerIsomorfismos(GuK1, GuK1)
    # obtener aristas de G y del complemento de GuK1
    aristasG = list(G.edges)
    compGuK1 = nx.complement(GuK1)
    compAristas = list(compGuK1.edges)
    ############################## ETAPA 2 ##############################
    # obtener permutaciones asociadas a reemplazos NO triviales locales y globales
    for (r, s) in aristasG:
        for (k, l) in compAristas:
            # tiempo inicial para impresion de avance
            tiempoInicial = time.time()
            # revisar condiciones de grados en GuK1 antes de realizar el reemplazo
            condicionesGrados = revisarCondicionesDeGrados(GuK1, r, s, k, l)
            # si se mantienen las condiciones de grados, se continua con el reemplazo en GuK1
            if(condicionesGrados):
                # realizar reemplazo sobre GuK1 para obtener GuK1-rs+kl
                graficaConReemplazo = aplicarReemplazo(GuK1, r, s, k, l)
                # revisar si GuK1-rs+kl es isomorfa a GuK1
                sonIsomorfas = nx.is_isomorphic(graficaConReemplazo, GuK1)
                # si son isomorfas, entonces calcular y guardar isomorfismos de GuK1-rs+kl en GuK1
                if(sonIsomorfas):
                    permutacionesGlobales = permutacionesGlobales + obtenerIsomorfismos(graficaConReemplazo, GuK1)
                    # si ademas k y l NO son el vertice nuevo n, continuar con el reemplazo en G
                    if(not (n in (k, l))):
                        # realizar reemplazo sobre G para obtener G-rs+kl
                        graficaConReemplazo = aplicarReemplazo(G, r, s, k, l)
                        # calcular y guardar isomorfismos de G-rs+kl en G
                        permutacionesLocales = permutacionesLocales + obtenerIsomorfismos(graficaConReemplazo, G)
            # tiempo final para impresion de avance e imprimir porcentaje de avance del analisis
            avance = avance + 1
            porcentaje = round((avance*100)/(len(aristasG)*len(compAristas)), 2)
            tiempoFinal = time.time()
            if(tiempoFinal - tiempoInicial >= factor):
                imprimirAvance(numG, totalGraficas, porcentaje)
    ############################## ETAPA 3 ##############################
    # analizar grupos generados
    grupoGeneradoLocal = PermutationGroup(permutacionesLocales)
    if(grupoGeneradoLocal.order() == factorial(n)):
        esLA = True
    if(esLA and (gradMin in (0, 1))):
        esGA = True
    else:
        if(1 in grados):
            grupoGeneradoGlobal = PermutationGroup(permutacionesGlobales)
            if(grupoGeneradoGlobal.order() == factorial(nMasUno)):
                esGA = True
    # determinar familia
    if(esLA and esGA):
        familiaG = "LAnGA"
    if(esLA and (not esGA)):
        familiaG = "LA"
    if((not esLA) and esGA):
        familiaG = "GA"
    if((not esLA) and (not esGA)):
        familiaG = "NO"
    # fin de funcion
    return(familiaG)


# Main #########################################################################


# mensaje
print("\n")
print(">>> Determine if a graph is amoeba or not - Standalone - [@MarcosLaffitte - Github Repo - Amoebas]")


# mensaje
print("\n")
print("* Building graph ...")
print("\n")


# INTRODUCIR GRAFICA AQUI
# como lista de aristas, despues comentar
# el ejemplo y SIEMPRE nombrar como G
# a la variable que guarda la grafica
# ejemplo: C3 con manita
G = nx.Graph()
G.add_edge(1, 2)
G.add_edge(2, 3)
G.add_edge(3, 1)
G.add_edge(3, 4)










# Analysis #####################################################################


# ANALISIS, no cambiar: la conversion-desconversion
# se agrega para que el usuario pueda introducir
# vertices con "nombres" arbitrarios, ya que el
# procesamiento requiere vertices de 0 a n-1
someBytes = nx.to_graph6_bytes(G, header = False)
eachG6 = someBytes.decode()
eachG6 = eachG6.rstrip("\n")
convGraph = nx.from_graph6_bytes(eachG6.encode())
orden = convGraph.order()
tamano = convGraph.size()
# analizar grafica
if(tamano == 0):
    familia = "LAnGA"
else:
    familia = analizarAmoebasGraficasArbitrarias(convGraph, 1, 1)


# finalizar barra de avance completada
imprimirAvance(1, 1, 100)


# mensaje
print("\n")
print("* Completed analysis ...")


# guardar resultado
resultado = (eachG6, orden, tamano, familia)


# mensaje
print("\n")
familiaStr = ""
if(familia == "LA"):
    familiaStr = "Local-But-Not-Global Amoeba"
if(familia == "GA"):
    familiaStr = "Global-But-Not-Local Amoeba"
if(familia == "LAnGA"):
    familiaStr = "Local-And-Global Amoeba"
if(familia == "NO"):
    familiaStr = "Not an Amoeba"
print("* The given graph was: " + familiaStr)


# mensaje
print("\n")
print("* Making plot of graph ...")


# checar planaridad
posiciones = dict()
if(nx.check_planarity(G, counterexample = False)[0]):
    posiciones = nx.planar_layout(G)
else:
    posiciones = nx.spring_layout(G)


# dibujar grafica
nx.draw_networkx_nodes(G, pos = posiciones,
                       edgecolors = "k", linewidths = 2,
                       node_size = 350, node_color = "w")
nx.draw_networkx(G, pos = posiciones, with_labels = True,
                 width = 1.5, node_color = "w", font_size = 8)
# definir cadena de G6
nombreG6Str = "g6-string: " + eachG6
# definir cadena de orden y tamano
nmStr = "(order, size) = " + "(" + str(orden) + "," + str(tamano) + ")"
# agregar titulo
plt.title(nombreG6Str + "\n" + nmStr + "\n" + familiaStr, fontsize = 9)
# guardar figura
plt.savefig("Resultado.pdf")
plt.close()


# mensaje
print("\n")
print(">>> Finished")
print("\n")


# Fin ##########################################################################
################################################################################
