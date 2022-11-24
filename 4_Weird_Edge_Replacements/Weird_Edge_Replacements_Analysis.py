################################################################################
#                                                                              #
#  README - Programa: Weird_Edge_Replacements_Analysis.py                      #
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
#  - Descripcion: recibe una lista de graficas arbitrarias simples no nulas y  #
#    determina las amoebas y no amoebas, raras y ordinarias, junto con sus     #
#    reemplazos admisibles de aristas raros y ordinarios no triviales.         #
#  - Input: Lista de graficas   [Archivo*.g6]   en formato graph6 o g6         #
#  - Output: cuatro archivos                                                   #
#            1) [Archivo*]_Weird_Amoebas.pkl      (LA, GA, LAnGA)              #
#            2) [Archivo*]_Weird_Graphs.pkl       (no amoebas)                 #
#            3) [Archivo*]_Ordinary_Amoebas.pkl   (LA, GA, LAnGA)              #
#            4) [Archivo*]_Ordinary_Graphs.pkl    (no amoebas)                 #
#  - Ejecutar como:                                                            #
#        python3.7  Weird_Edge_Replacements_Analysis.py  [Archivo*.g6]         #
#                                                                              #
#  - Fecha: 22 de abril 2022                                                   #
#                                                                              #
#  * las variables se nombran con formato estilo java                          #
#  * en este analisis siempre se realizan la ETAPA 1 y ETAPA 2 mencionadas en  #
#    la tesis, para poder determinar los reemplazos raros de cada grafica      #
#  * Sympy requiere que los vertices sean enteros {0, 1, ..., n-1}             #
#                                                                              #
################################################################################


# Requiere #####################################################################


"""
> Lenguaje: python 3.7
> Anaconda: 4-bit version - conda 4.10.1
> Paquetes:  (instalados con anaconda)
***** networkx 2.5
***** sympy 1.7.1
"""


# Dependencias #################################################################


# instaladas con conda ---------------------------------------------------------
import networkx as nx
from networkx.algorithms import isomorphism
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics.perm_groups import PermutationGroup


# incluidas en python ----------------------------------------------------------
import time
import pickle
from sys import argv
from copy import deepcopy
from math import factorial, modf


# Variables ####################################################################


# entrada ----------------------------------------------------------------------
inFileName = argv[1]
inFile = None
listaInput = []
totalGraficas = 0


# salida -----------------------------------------------------------------------
outFile = None
amoebasRaras = []
graficasRaras = []
amoebasOrdinarias = []
graficasOrdinarias = []
amoebasRarasFile = inFileName.split(".")[0] + "_Weird_Amoebas.pkl"
graficasRarasFile = inFileName.split(".")[0] + "_Weird_Graphs.pkl"
amoebasOrdinariasFile = inFileName.split(".")[0] + "_Ordinary_Amoebas.pkl"
graficasOrdinariasFile = inFileName.split(".")[0] + "_Ordinary_Graphs.pkl"


# datos ------------------------------------------------------------------------
resultado = ()      # (nombreG6, orden, tamano, familia, tipo, listaReemps)
orden = 0           # cantidad de vertices
tamano = 0          # cantidad de aristas
familia = ""        # solo "LA", solo "GA", "LAnGA", no amoeba "NO"
tipo = ""           # rara "R" u ordinaria "O"
# descripcion: reemplazo = ()      # reemplazo admisible (r, s, k, l)
# descripcion: listaReemps = []    # [[reemplazos ordinarios], [reemplazos raros]]


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


# funcion: revisar si un reemplazo admisible es ordinario en G -----------------
def revisarOrdinario(originalG, someVr, someVs, someVk, someVl):
    # variables locales
    copiaG = None
    isos = []        
    aristaImagen = {}
    eachIso = None
    reemplazoOrdinario = False    
    # hacer reemplazo y calcular isomorfismos
    copiaG = aplicarReemplazo(originalG, someVr, someVs, someVk, someVl)    
    isos = obtenerIsomorfismos(copiaG, originalG)
    # buscar isomorfismo que mande {vk, vl} en {vr, vs}
    for eachIso in isos:
        # en esta parte k^eachIso denota eachIso(k)
        aristaImagen = {someVk^eachIso, someVl^eachIso}
        if(aristaImagen == {someVr, someVs}):
            reemplazoOrdinario = True
            break
    # fin de funcion
    return(reemplazoOrdinario)


# funcion: deteccion de amoebas y reemplazos raros - en G no vacía!!! ----------
def analizarAmoebasReemplazosRaros(G, numG, totalGraficas):
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
    ordinario = False
    reempsO = []    
    reempsR = []
    grados = []
    gradMin = 0
    gradMax = 0
    gradosTot = 0
    gradosCompletos = False
    familiaG = ""
    tipoG = ""
    listaReempsG = []    
    avance = 0
    porcentaje = 0
    tiempoInicial = 0
    tiempoFinal = 0
    ############################## ETAPA 1 ##############################
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
                        # determinar si rs -> kl es raro u ordinario y guardarlo en su respectiva lista
                        ordinario = revisarOrdinario(G, r, s, k, l)
                        if(ordinario):
                            reempsO.append((r, s, k, l))
                        else:
                            reempsR.append((r, s, k, l))
            # tiempo final para impresion de avance e imprimir porcentaje de avance del analisis
            avance = avance + 1
            porcentaje = round((avance*100)/(len(aristasG)*len(compAristas)), 2)
            tiempoFinal = time.time()
            if(tiempoFinal - tiempoInicial >= factor):
                imprimirAvance(numG, totalGraficas, porcentaje)
    ############################## ETAPA 3 ##############################
    # analizar conjuto de grados de G
    grados = list(set([d for (v, d) in list(G.degree())]))
    gradMin = min(grados)
    gradMax = max(grados)
    gradosTot = len(grados)
    if(gradosTot == (gradMax - (gradMin - 1))):
        gradosCompletos = True
    # analizar grupos generados
    if(gradosCompletos):
        grupoGeneradoLocal = PermutationGroup(permutacionesLocales)
        if(grupoGeneradoLocal.order() == factorial(n)):
            esLA = True
    if(esLA and (gradMin in (0, 1))):
        esGA = True
    else:
        if((1 in grados) and gradosCompletos):
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
    # determinar tipo
    if(len(reempsR) == 0):
        tipoG = "O"
    else:
        tipoG = "R"
    # determinar lista de reemplazos
    listaReempsG = [reempsO, reempsR]
    # fin de funcion
    return(familiaG, tipoG, listaReempsG)


# Main #########################################################################


# mensaje inicial
print("\n")
print(">>> Weird Edge-Replacements - Analysis - [@MarcosLaffitte - Github Repo - Amoebas]")
print("\n")


# obtener lista de graficas a analizar en formato g6
inFile = open(inFileName, "r")
listaInput = inFile.readlines() 
inFile.close()
listaInput = [eachGraph.rstrip("\n") for eachGraph in listaInput]
totalGraficas = len(listaInput)


# determinar amoebas y sus propiedades
for indice in range(totalGraficas):
    # reinicializar barra de avance
    imprimirAvance(indice+1, totalGraficas, 0)    
    # reinicializar grafica para analisis
    eachG6 = listaInput[indice]
    eachGraph = nx.from_graph6_bytes(eachG6.encode())
    # guardar orden y tamano de la grafica
    orden = eachGraph.order()
    tamano = eachGraph.size()    
    # analizar grafica
    if(tamano == 0):
        familia = "LAnGA"
        tipo = "O"
        listaReemps = [[],[]]
    else:
        (familia, tipo, listaReemps) = analizarAmoebasReemplazosRaros(eachGraph, indice+1, totalGraficas)
    # guardar grafica en su lista correspondiente
    resultado = (eachG6, orden, tamano, familia, tipo, listaReemps)
    if(familia in ("LA", "GA", "LAnGA")):
        if(tipo == "R"):
            amoebasRaras.append(resultado)
        if(tipo == "O"):
            amoebasOrdinarias.append(resultado)
    else:
        if(tipo == "R"):
            graficasRaras.append(resultado)            
        if(tipo == "O"):
            graficasOrdinarias.append(resultado)


# finalizar barra de avance completada
imprimirAvance(totalGraficas, totalGraficas, 100)

            
# mensaje de completado
print("\n")
print("* Completed analysis ...")
            
            
# mensaje de guardar datos
print("\n")
print("* Saving data ...")


# 1) amoebas raras
outFile = open(amoebasRarasFile, "wb")
pickle.dump(amoebasRaras, outFile)                      
outFile.close() 


# 2) graficas raras
outFile = open(graficasRarasFile, "wb")
pickle.dump(graficasRaras, outFile)                      
outFile.close() 


# 3) amoebas ordinarias
outFile = open(amoebasOrdinariasFile, "wb")
pickle.dump(amoebasOrdinarias, outFile)                      
outFile.close() 


# 4) graficas ordinarias
outFile = open(graficasOrdinariasFile, "wb")
pickle.dump(graficasOrdinarias, outFile)                      
outFile.close() 


# mensaje resumen
print("\n")
print("* Summary - Tot. analyzed graphs: " + str(totalGraficas))
print("- Weird Amoebas: ", len(amoebasRaras))
print("- Weird Graphs (Not Amoeba): ", len(graficasRaras))
print("- Ordinary Amoebas: ", len(amoebasOrdinarias))
print("- Ordinary Graphs (Not Amoeba): ", len(graficasOrdinarias))


# mensaje final
print("\n")
print(">>> Finished")
print("\n")


# Fin ##########################################################################
################################################################################
