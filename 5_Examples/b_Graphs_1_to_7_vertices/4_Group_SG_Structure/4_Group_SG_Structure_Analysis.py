################################################################################
#                                                                              #
#  README - Programa: 4_Estructura_SG_Analisis.py                              #
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
#  - Descripcion: recibe una lista de graficas arbitrarias simples no nulas y  #
#    determina las amoebas y no amoebas, junto con la estructura de los grupos #
#    S_G y S_GuK1 de cada grafica G en la lista por medio de SageMath.         #
#    Si ademas G es una grafica rara, el programa calcula adicionalmente la    #
#    la estructura de SG y S_GuK1 que se obtiene solo tomando en cuenta        #
#    primero reemplazos raros y luego solo a los ordinarios.                   #
#  - Input: Lista de graficas   [Archivo*.g6]   en formato graph6 o g6         #
#  - Output: cuatro archivos                                                   #
#            1) [Archivo*]_grupoSG_LA.pkl         (solo LA)                    #
#            2) [Archivo*]_grupoSG_GA.pkl         (solo GA)                    #
#            3) [Archivo*]_grupoSG_LAnGA.pkl      (LA y GA)                    #
#            4) [Archivo*]_grupoSG_No_Amoeba.pkl  (graficas no amoebas)        #
#  - Ejecutar como:                                                            #
#        python3.7  4_Estructura_SG_Analisis.py  [Archivo*.g6]                 #
#                                                                              #
#                o tambien con el python de sage como                          #
#                                                                              #
#        sage  -python   4_Estructura_SG_Analisis.py  [Archivo*.g6]            #
#                                                                              #
#  - Fecha: 22 de abril 2022                                                   #
#                                                                              #
#  * las variables se nombran con formato estilo java                          #
#  * en este analisis siempre se realizan la ETAPA 1 y ETAPA 2 mencionadas en  #
#    la tesis, para determinar la estructura de los grupos SG y SGuK1          #
#  * SageMath requiere que los vertices sean enteros {1, 2, ..., n}            #
#                                                                              #
################################################################################


# Requiere #####################################################################


"""
> Lenguaje: python 3.7
> Anaconda: 4-bit version - conda 4.10.1
> Paquetes: (instalados con anaconda)
***** networkx 2.5
***** sage 9.2
"""


# Dependencias #################################################################


# instaladas con conda ---------------------------------------------------------
import networkx as nx
from networkx.algorithms import isomorphism
from sage.all import *


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
amoebasLA = []
amoebasGA = []
amoebasLAnGA = []
graficasNoAmoeba = []
amoebasLAFile = inFileName.split(".")[0] + "_groupSG_LA.pkl"
amoebasGAFile = inFileName.split(".")[0] + "_groupSG_GA.pkl"
amoebasLAnGAFile = inFileName.split(".")[0] + "_groupSG_LAnGA.pkl"
graficasNoAmoebaFile = inFileName.split(".")[0] + "_groupSG_Not_Amoeba.pkl"


# datos ------------------------------------------------------------------------
resultado = ()     # (nombreG6, orden, tamano, familia, tipo, estructuras)
orden = 0          # cantidad de vertices
tamano = 0         # cantidad de aristas
familia = ""       # solo "LA", solo "GA", "LAnGA", no amoeba "NO"
tipo = ""          # rara "Weird" u ordinaria "Ordinary"
estructuras = []   # estructuras = [estSG, estSGRaro, estSGOrd, estSGuK1, estSGuK1Raro, estSGuK1Ord]
# descripcion: estSG = ""         # e.g. S_n, C_n, A_n, ...
# descripcion: estSGRaro = ""     # SG generado sin reemplazos raros
# descripcion: estSGOrd = ""      # SG generado sin reemplazos ordinarios
# descripcion: estSGuK1 = ""      # e.g. S_n+1, C_n+1, A_n+1, ...
# descripcion: estSGuK1Raro = ""  # SGuK1 generado sin reemplazos raros
# descripcion: estSGuK1Ord = ""   # SGuK1 generado sin reemplazos ordinarios


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
    # convertir isomorfismo a lista [f(1), f(2), ..., f(n)]
    for i in range(1, len(isoDict) + 1):
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
    isosComoPermutaciones = [isoListVersion(iso) for iso in isomorfismos]
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
    matcher = isomorphism.GraphMatcher(copiaG, originalG)
    isos = list(matcher.isomorphisms_iter())
    # buscar isomorfismo que mande {vk, vl} en {vr, vs}
    for eachIso in isos:
        aristaImagen = {eachIso[someVk], eachIso[someVl]}
        if(aristaImagen == {someVr, someVs}):
            reemplazoOrdinario = True
            break
    # fin de funcion
    return(reemplazoOrdinario)


# funcion: deteccion de amoebas y estructura de SG y SGuK1 ---------------------
def analizarAmoebasEstructuraDeGrupos(G, numG, totalGraficas):
    # variables globales
    global factor
    # variables locales
    esLA = False
    esGA = False
    aristasG = []    
    GuK1 = None
    compGuK1 = None
    compAristas = []
    n = 0                             # orden de G
    nMasUno = 0                       # orden de GuK1
    permutacionesLocalesRaras = []    # asociadas a reemplazos raros de G
    permutacionesLocalesOrds = []     # asociadas a reemplazos ordinarios de G
    permutacionesGlobalesRaras = []   # asociadas a reemplazos raros de GuK1
    permutacionesGlobalesOrds = []    # asociadas a reemplazos ordinarios de GuK1
    grupoGeneradoLocalRaro = None     # grupo S_G generado por reemplazos raros de G
    grupoGeneradoLocalOrd = None      # grupo S_G generado por reemplazos ordinarios de G
    grupoGeneradoLocal = None         # grupo S_G generado por todo reemplazo admisible de G
    grupoGeneradoGlobalRaro = None    # grupo S_GuK1 generado por reemplazos raros de GuK1
    grupoGeneradoGlobalOrd = None     # grupo S_GuK1 generado por reemplazos ordinarios de GuK1
    grupoGeneradoGlobal = None        # grupo S_GuK1 generado por todo reemplazo admisible de GuK1
    estructuraGrupoLocalRaro = ""     # (unico) subgrupo de Sn isomorfo a SG con reemplazos raros
    estructuraGrupoLocalOrd = ""      # (unico) subgrupo de Sn isomorfo a SG con reemplazos ordinarios
    estructuraGrupoLocal = ""         # (unico) subgrupo de Sn isomorfo a SG con todo reemplazo admisible
    estructuraGrupoGlobalRaro = ""    # (unico) subgrupo de Sn+1 isomorfo a SGuK1 con reemplazos raros
    estructuraGrupoGlobalOrd = ""     # (unico) subgrupo de Sn+1 isomorfo a SGuK1 con reemplazos ordinarios
    estructuraGrupoGlobal = ""        # (unico) subgrupo de Sn+1 isomorfo a SGuK1 con todo reemplazo admisible
    r = 0
    s = 0
    k = 0
    l = 0    
    condicionesLilith = False    
    graficaConReemplazo = None
    sonIsomorfas = False
    ordinario = False
    graficaRara = False
    familiaG = ""
    avance = 0
    porcentaje = 0
    tiempoInicial = 0
    tiempoFinal = 0
    ############################## ETAPA 1 ##############################
    # obtener n y nMasUno para dar nombre "n+1" a nuevo vertice aislado
    n = G.order()
    nMasUno = n + 1    
    GuK1 = deepcopy(G)
    GuK1.add_node(nMasUno)
    # calcular automorfismos de G; permutaciones locales asociadas a todo reemplazo trivial
    permutacionesLocalesOrds = permutacionesLocalesOrds + obtenerIsomorfismos(G, G)
    # calcular automorfismos de GuK1; permutaciones globales asociadas a todo reemplazo trivial
    permutacionesGlobalesOrds = permutacionesGlobalesOrds + obtenerIsomorfismos(GuK1, GuK1)
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
            # revisar condiciones de Lilith en GuK1 antes de realizar el reemplazo
            condicionesLilith = revisarCondicionesLilith(GuK1, r, s, k, l)
            # si se mantienen las condiciones de lilith, se continua con el reemplazo en GuK1
            if(condicionesLilith):
                # realizar reemplazo sobre GuK1 para obtener GuK1-rs+kl
                graficaConReemplazo = aplicarReemplazo(GuK1, r, s, k, l)
                # revisar si GuK1-rs+kl es isomorfa a GuK1
                sonIsomorfas = nx.is_isomorphic(graficaConReemplazo, GuK1)
                # si son isomorfas, entonces calcular y guardar isomorfismos de GuK1-rs+kl en GuK1 
                if(sonIsomorfas):
                    # determinar si rs -> kl es ordinario en GuK1 (y por ende en G de ser el caso)
                    ordinario = revisarOrdinario(GuK1, r, s, k, l)
                    # guardar permutaciones dependiendo de si el reemplazo es raro u ordinario
                    if(ordinario):
                        permutacionesGlobalesOrds = permutacionesGlobalesOrds + obtenerIsomorfismos(graficaConReemplazo, GuK1)
                    else:
                        permutacionesGlobalesRaras = permutacionesGlobalesRaras + obtenerIsomorfismos(graficaConReemplazo, GuK1)
                        graficaRara = True
                    # si ademas k y l NO son el vertice nuevo n+1, continuar con el reemplazo en G
                    if(not (nMasUno in (k, l))):
                        # realizar reemplazo sobre G para obtener G-rs+kl
                        graficaConReemplazo = aplicarReemplazo(G, r, s, k, l)                    
                        # calcular y guardar isomorfismos de G-rs+kl en G dependiendo de si es raro u ordinario
                        if(ordinario):
                            permutacionesLocalesOrds = permutacionesLocalesOrds + obtenerIsomorfismos(graficaConReemplazo, G)
                        else:
                            permutacionesLocalesRaras = permutacionesLocalesRaras + obtenerIsomorfismos(graficaConReemplazo, G)
            # tiempo final para impresion de avance e imprimir porcentaje de avance del analisis
            avance = avance + 1
            porcentaje = round((avance*100)/(len(aristasG)*len(compAristas)), 2)
            tiempoFinal = time.time()
            if(tiempoFinal - tiempoInicial >= factor):
                imprimirAvance(numG, totalGraficas, porcentaje)
    ############################## ETAPA 3 ##############################
    # analizar grupos generados y sus estructuras
    grupoGeneradoLocal = PermutationGroup(permutacionesLocalesOrds + permutacionesLocalesRaras)
    estructuraGrupoLocal = grupoGeneradoLocal.structure_description()    
    if(graficaRara):
        grupoGeneradoLocalRaro = PermutationGroup(permutacionesLocalesRaras)
        estructuraGrupoLocalRaro = grupoGeneradoLocalRaro.structure_description()
        grupoGeneradoLocalOrd = PermutationGroup(permutacionesLocalesOrds)
        estructuraGrupoLocalOrd = grupoGeneradoLocalOrd.structure_description()    
    if(grupoGeneradoLocal.order() == factorial(n)):
        esLA = True
    grupoGeneradoGlobal = PermutationGroup(permutacionesGlobalesOrds + permutacionesGlobalesRaras)
    estructuraGrupoGlobal = grupoGeneradoGlobal.structure_description()            
    if(graficaRara):        
        grupoGeneradoGlobalRaro = PermutationGroup(permutacionesGlobalesRaras)
        estructuraGrupoGlobalRaro = grupoGeneradoGlobalRaro.structure_description()
        grupoGeneradoGlobalOrd = PermutationGroup(permutacionesGlobalesOrds)
        estructuraGrupoGlobalOrd = grupoGeneradoGlobalOrd.structure_description()
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
    if(graficaRara):
        return(familiaG, "Weird",
               [estructuraGrupoLocal, estructuraGrupoLocalRaro, estructuraGrupoLocalOrd,
               estructuraGrupoGlobal, estructuraGrupoGlobalRaro, estructuraGrupoGlobalOrd])
    else:
        return(familiaG, "Ordinary",
               [estructuraGrupoLocal, "-", "-",
               estructuraGrupoGlobal, "-", "-"])        


# Main #########################################################################


# mensaje inicial
print("\n")
print(">>> Structure of the SG and SGuK1 groups - Analysis - [@MarcosLaffitte - Github Repo - Amoebas]")
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
    # renombrar los vertices de 1 a n para SageMath, porque la conversion G6 los nombra como 0 a n-1
    eachGraph = nx.convert_node_labels_to_integers(eachGraph, first_label = 1, ordering = "sorted")
    # guardar orden y tamano de la grafica
    orden = eachGraph.order()
    tamano = eachGraph.size()    
    # analizar grafica
    (familia, tipo, estructuras) = analizarAmoebasEstructuraDeGrupos(eachGraph, indice+1, totalGraficas)
    # guardar grafica en su lista correspondiente    
    resultado = (eachG6, orden, tamano, familia, tipo, estructuras)
    if(familia == "LA"):
        amoebasLA.append(resultado)
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


# 1) amoebas solo LA
outFile = open(amoebasLAFile, "wb")
pickle.dump(amoebasLA, outFile)                      
outFile.close() 


# 2) amoebas solo GA
outFile = open(amoebasGAFile, "wb")
pickle.dump(amoebasGA, outFile)                      
outFile.close() 


# 3) amoebas LAnGA
outFile = open(amoebasLAnGAFile, "wb")
pickle.dump(amoebasLAnGA, outFile)                      
outFile.close() 


# 4) graficas No Amoeba
outFile = open(graficasNoAmoebaFile, "wb")
pickle.dump(graficasNoAmoeba, outFile)                      
outFile.close() 


# mensaje resumen
print("\n")
print("* Summary - Tot. analyzed graphs: " + str(totalGraficas))
print("- Local-But-Not-Global Amoebas: ", len(amoebasLA))
print("- Global-But-Not-Local Amoebas: ", len(amoebasGA))
print("- Local-And-Global Amoebas: ", len(amoebasLAnGA))
print("- Not-Amoeba Graphs: ", len(graficasNoAmoeba))


# mensaje final
print("\n")
print(">>> Finished")
print("\n")


# Fin ##########################################################################
################################################################################
