################################################################################
#                                                                              #
#  README - Programa: 2_Detector_Amoebas_Arbol_Analisis.py                     #
#                                                                              #
#  - Hecho por: Lic. Marcos Emmanuel Gonzalez Laffitte                         #
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
#  - Tesis UNAM:  www...                                                       #
#  - Descripcion: recibe una lista de arboles no nulos y determina entre       #
#    ellos a las amoebas y no amoebas.                                         #
#  - Input: Lista de graficas   [Archivo*.g6]   en formato graph6 o g6         #
#  - Output: tres archivos                                                     #
#            1) [Archivo*]_arboles_GA.pkl         (solo GA)                    #
#            2) [Archivo*]_arboles_LAnGA.pkl      (LA y GA)                    #
#            3) [Archivo*]_arboles_No_Amoeba.pkl  (arboles no amoebas)         #
#  - Ejecutar como:                                                            #
#       python3.7  2_Detector_Amoebas_Arbol_Analisis.py  [Archivo*.g6]         #
#                                                                              #
#  - Fecha: 22 de abril 2022                                                   #
#                                                                              #
#  * las variables se nombran con formato estilo java                          #
#  * en este analisis si se evitan las etapas ETAPA 1, ETAPA 2, ETAPA 2 y      #
#    ETAPA 4 mencionadas en la tesis, dependiendo del conjunto de grados de T  #
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
from itertools import product
from math import factorial, modf


# Variables ####################################################################


# entrada ----------------------------------------------------------------------
inFileName = argv[1]
inFile = None
listaInput = []
totalGraficas = 0


# salida -----------------------------------------------------------------------
outFile = None
amoebasGA = []
amoebasLAnGA = []
graficasNoAmoeba = []
amoebasGAFile = inFileName.split(".")[0] + "_trees_GA.pkl"
amoebasLAnGAFile = inFileName.split(".")[0] + "_trees_LAnGA.pkl"
graficasNoAmoebaFile = inFileName.split(".")[0] + "_trees_Not_Amoeba.pkl"


# datos ------------------------------------------------------------------------
resultado = ()      # (nombreG6, orden, tamano, familia)
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


# funcion: revisar las condiciones de Lilith sobre los grados ------------------
def revisarCondicionesLilith(someG, vr, vs, vk, vl):
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
        # si {d(vk) + 1, d(vl) + 1} = {d(vr), d(vs)}, se mantienen las condiciones de Lilith
        if(gradosOriginal == gradosNuevos):
            condicion = True
    # analizar caso  ii) |{r, s} n {k, l}| = 1
    if(len({vr, vs}.intersection({vk, vl})) == 1):        
        conservado = list({vr, vs}.intersection({vk, vl}))[0]
        va = list({vr, vs}.difference({conservado}))[0]
        vb = list({vk, vl}.difference({conservado}))[0]
        da = someG.degree(va)
        db = someG.degree(vb)
        # si d(vb) + 1 = d(va), se mantienen las condiciones de Lilith
        if(db + 1 == da):
            condicion = True
    # fin de funcion
    return(condicion)


# funcion: obtener aristas entre componentes conexas de T-vrvs -----------------
def aristasEntreComponentes(T, vr, vs):
    # variables locales
    copiaT = None    
    componentes = []    
    aristasValidas = []
    # tomar aristas en el complemento de T-vrvs que si den un arbol en el reemplazo
    copiaT = deepcopy(T)
    copiaT.remove_edge(vr, vs)
    componentes = list(nx.connected_components(copiaT))
    aristasValidas = list(product(list(componentes[0]), list(componentes[1])))
    if((vr, vs) in aristasValidas):            
        aristasValidas.remove((vr, vs))
    else:
        aristasValidas.remove((vs, vr))    
    # fin de funcion
    return(aristasValidas)
  

# funcion: deteccion de amoebas entre arboles no triviales ---------------------
def analizarAmoebasArbol(G, numG, totalGraficas):
    # variables globales
    global factor
    # variables locales
    aristasG = []    
    GuK1 = None
    n = 0                          # orden de G
    nMasUno = 0                    # orden de GuK1
    permutacionesLocales = []      # asociadas a reemplazos admisibles de G
    permutacionesGlobales = []     # asociadas a reemplazos admisibles de GuK1
    grupoGeneradoLocal = None      # grupo S_G
    grupoGeneradoGlobal = None     # grupo S_GuK1
    aristasCompComp = []           # aristas validas entre componentes conexas de T-rs
    aristasExteriores = []         # aristas incluyendo al nuevo vertice
    aislado = None                 # unico vertice aislado en T-rs+kl    
    r = 0
    s = 0
    k = 0
    l = 0
    condicionesLilith = False    
    graficaConReemplazo = None
    sonIsomorfas = False
    grados = []
    gradMin = 0
    gradMax = 0
    gradosTot = 0
    gradosCompletos = False
    avance = 0
    porcentaje = 0
    tiempoInicial = 0
    tiempoFinal = 0
    ############################## GRADOS ###############################
    # analizar conjunto de grados; aunque siempre gradMin = 1, se deja asi por reusabilidad y conceptos 
    grados = list(set([d for (v, d) in list(G.degree())]))
    gradMin = min(grados)
    gradMax = max(grados)
    gradosTot = len(grados)
    if(not (gradosTot == (gradMax - (gradMin - 1)))):     
        return("NO")
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
    # obtener aristas de G
    aristasG = list(G.edges)
    ############################## ETAPA 2 ##############################
    # obtener permutaciones asociadas a reemplazos locales NO triviales
    for (r, s) in aristasG:
        # obtener aristas validas entre componentes de G-rs
        aristasCompComp = aristasEntreComponentes(G, r, s)
        # tiempo inicial para impresion de avance
        tiempoInicial = time.time()
        for (k, l) in aristasCompComp:
            # revisar condiciones de Lilith en G antes de realizar el reemplazo
            condicionesLilith = revisarCondicionesLilith(G, r, s, k, l)
            # si se mantienen las condiciones de lilith, se continua con el reemplazo en G
            if(condicionesLilith):
                # realizar reemplazo sobre G para obtener G-rs+kl
                graficaConReemplazo = aplicarReemplazo(G, r, s, k, l)        
                # revisar si G-rs+kl es isomorfa a G
                sonIsomorfas = isomorphism.tree_isomorphism(graficaConReemplazo, G)
                # si son isomorfas, entonces calcular y guardar isomorfismos tanto locales como globales
                if(sonIsomorfas):
                    # obtener permutaciones locales
                    permutacionesLocales = permutacionesLocales + obtenerIsomorfismos(graficaConReemplazo, G)
                    # obtener permutaciones globales
                    graficaConReemplazo = aplicarReemplazo(GuK1, r, s, k, l)                            
                    permutacionesGlobales = permutacionesGlobales + obtenerIsomorfismos(graficaConReemplazo, GuK1)
        # tiempo final para impresion de avance e imprimir porcentaje de avance del analisis
        avance = avance + 1
        porcentaje = round((avance*100)/(2*len(aristasG)), 2)
        tiempoFinal = time.time()
        if(tiempoFinal - tiempoInicial >= factor):
            imprimirAvance(numG, totalGraficas, porcentaje)
    # si G es LA, entonces tambien es GA
    grupoGeneradoLocal = PermutationGroup(permutacionesLocales)
    if(grupoGeneradoLocal.order() == factorial(n)):
        return("LAnGA")
    ############################## ETAPA 3 ##############################
    # obtener aristas de los vertices de G contra el nuevo vertice "n" en GuK1
    aristasExteriores = list(product([n], list(G.nodes())))
    # obtener permutaciones asociadas a reemplazos de arista globales o exteriores
    avance = 0
    for (r, s) in aristasG:
        for (k, l) in aristasExteriores:
            # tiempo inicial para impresion de avance
            tiempoInicial = time.time()
            # revisar condiciones de Lilith en GuK1 antes de realizar el reemplazo
            condicionesLilith = revisarCondicionesLilith(GuK1, r, s, k, l)
            # si se mantienen las condiciones de lilith, se continua con el reemplazo en GuK1
            if(condicionesLilith):
                # realizar reemplazo sobre GuK1 para obtener GuK1-rs+kl
                graficaConReemplazo = aplicarReemplazo(GuK1, r, s, k, l)        
                # remover el unico vertice aislado de GuK1-rs+kl (garantizado por las condiciones de Lilith)
                aislado = [v for v in list(graficaConReemplazo.nodes()) if graficaConReemplazo.degree(v) == 0][0]
                graficaConReemplazo.remove_node(aislado)
                # revisar si la "componente arbol" de GuK1-rs+kl es isomorfa a la "componente arbol", i.e. G, de GuK1
                sonIsomorfas = isomorphism.tree_isomorphism(graficaConReemplazo, G)
                # si son isomorfas, entonces calcular y guardar isomorfismos globales
                if(sonIsomorfas):
                    # agregar nuevamente vertice aislado
                    graficaConReemplazo.add_node(aislado)
                    # obtener permutaciones globales
                    permutacionesGlobales = permutacionesGlobales + obtenerIsomorfismos(graficaConReemplazo, GuK1)
            # tiempo final para impresion de avance e imprimir porcentaje de avance del analisis
            avance = avance + 1
            porcentaje = 50 + round((avance*100)/(2*len(aristasG)*len(aristasExteriores)), 2)
            tiempoFinal = time.time()
            if(tiempoFinal - tiempoInicial >= factor):
                imprimirAvance(numG, totalGraficas, porcentaje)                           
    ############################## ETAPA 4 ##############################    
    # analizar grupo de permutaciones globales
    grupoGeneradoGlobal = PermutationGroup(permutacionesGlobales)
    if(grupoGeneradoGlobal.order() == factorial(nMasUno)):
        return("GA")
    else:
        return("NO")
    # fin de funcion

    
# Main #########################################################################


# mensaje inicial
print("\n")
print(">>> Detect Amoebas within a Set of Trees - Analysis - [@MarcosLaffitte - Github Repo - Amoebas]")
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
    # si no es arbol, pasar a otra grafica
    if((nx.is_connected(eachGraph)) and (tamano == orden-1)):
        # analizar grafica
        if(tamano == 0):
            familia = "LAnGA"
        else:
            familia = analizarAmoebasArbol(eachGraph, indice+1, totalGraficas)
        # guardar arbol en su lista correspondiente
        resultado = (eachG6, orden, tamano, familia)
        if(familia == "GA"):
            amoebasGA.append(resultado)
        if(familia == "LAnGA"):
            amoebasLAnGA.append(resultado)
        if(familia == "NO"):
            graficasNoAmoeba.append(resultado)


# finalizar barra de avance completada
imprimirAvance(totalGraficas, totalGraficas, 100)

            
# mensaje de completado
print("\n")
print("* Completed analysis ...")
            
            
# mensaje de guardar datos
print("\n")
print("* Saving data ...")


# 1) arboles amoeba solo GA
outFile = open(amoebasGAFile, "wb")
pickle.dump(amoebasGA, outFile)                      
outFile.close() 


# 2) arboles amoeba LAnGA
outFile = open(amoebasLAnGAFile, "wb")
pickle.dump(amoebasLAnGA, outFile)                      
outFile.close() 


# 3) arboles No Amoeba
outFile = open(graficasNoAmoebaFile, "wb")
pickle.dump(graficasNoAmoeba, outFile)                      
outFile.close() 


# mensaje resumen
print("\n")
print("* Summary - Tot. analyzed graphs: " + str(totalGraficas))
print("- Tot. analyzed trees: ", len(amoebasGA) + len(amoebasLAnGA) + len(graficasNoAmoeba))
print("- Global-But-Not-Local Amoeba Trees: ", len(amoebasGA))
print("- Local-And-Global Amoeba Trees: ", len(amoebasLAnGA))
print("- Not-Amoeba Trees: ", len(graficasNoAmoeba))


# mensaje final
print("\n")
print(">>> Finished")
print("\n")


# Fin ##########################################################################
################################################################################
