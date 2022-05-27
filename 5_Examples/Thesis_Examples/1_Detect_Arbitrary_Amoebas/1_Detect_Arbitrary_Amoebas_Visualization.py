################################################################################
#                                                                              #
#  README - Programa: 1_Detector_Amoebas_Arbitrarias_Visualizacion.py          #
#                                                                              #
#  - Hecho por: Lic. Marcos Emmanuel Gonzalez Laffitte                         #
#  - Github: @MarcosLaffitte                                                   #
#  - Repositiorio:  www...                                                     #
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
#  - Descripcion: recibe los 4 archivos de amoebas y graficas producidos por   #
#    1_Detector_Amoebas_Arbitrarias_Analisis.py, y genera (a lo mas) cuatro    #
#    archivos con dibujos de todas las graficas dadas.                         #
#  - Input:  4 archivos [Archivo*]_graficas_[LA/GA/LAnGA/No_Amoeba].pkl        #
#  - Output: cuatro archivos pdfs con los dibujos de las graficas dadas,       #
#            1) [Archivo*]_graficas_LA.pdf         (solo LA)                   #
#            2) [Archivo*]_graficas_GA.pdf         (solo GA)                   #
#            3) [Archivo*]_graficas_LAnGA.pdf      (LA y GA)                   #
#            4) [Archivo*]_graficas_No_Amoeba.pdf  (graficas no amoebas)       #
#  - Ejecutar como:                                                            #
#       python3.7  1_Detector_Amoebas_Arbitrarias_Visualizacion.py  *.pkl      #
#                                                                              #
#  * en linea de comandos literalmente poner "*.pkl" y python toma todo *.pkl  #
#  * poniendo solo los 4 archivos *.pkl en la misma carpeta que este script.   #
#  * los 4 archivos *.pkl deben estar nombrados con el formato de Output de    #
#    1_Detector_Amoebas_Arbitrarias_Analisis.py, de otra forma no se           #
#    ejecuta el programa.                                                      #
#                                                                              #
#  - Fecha: 26 de abril 2022                                                   #
#  * las variables se nombran con formato estilo java                          #
#                                                                              #
################################################################################


# Requiere #####################################################################


"""
> Lenguaje: python 3.7
> Anaconda: 4-bit version - conda 4.10.1
> Paquetes: (instalados con anaconda)
***** networkx 2.5
***** matplotlib 3.3.3
"""


# Dependencias #################################################################


# instaladas con conda ---------------------------------------------------------
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.backends.backend_pdf
from matplotlib.patches import Rectangle


# incluidas en python ----------------------------------------------------------
import pickle
from math import modf
from sys import argv, exit


# apagar warnings y matplotlib en backend para correr en servidor --------------
import warnings
matplotlib.use("Agg")
warnings.filterwarnings("ignore")


# Variables ####################################################################


# entrada y condiciones para continuar -----------------------------------------
inFile = None
archivos = argv[1:]   # archivos en el orden dado por el sistema
entrada1 = "graphs_LA."
entrada2 = "graphs_GA."
entrada3 = "graphs_LAnGA."
entrada4 = "graphs_Not_Amoeba."
continuar = False
listaArchivos = []    # archivos en el orden de las entradas
amoebasLA = []
amoebasGA = []
amoebasLAnGA = []
graficasNoAmoeba = []


# salida nombres de pdf's ------------------------------------------------------
amoebasLAFile = ""
amoebasGAFile = ""
amoebasLAnGAFile = ""
graficasNoAmoebaFile = ""


# Funciones ####################################################################


# funcion: revisar condiciones para ejecutar programa --------------------------
def condicionesDeEntrada(archivosDeEntrada):
    # variables globales
    global entrada1
    global entrada2
    global entrada3
    global entrada4
    # variables locales
    listaEntradas = [entrada1, entrada2, entrada3, entrada4]
    siEntradas = [False, False, False, False]    
    cuatroPKLs = False    
    eachArchivo = ""
    archivosEnOrden = []
    # revisar cantidad de archivos
    if(len(archivosDeEntrada) == 4):
        cuatroPKLs = True
    # revisar que si esten todos los tipos de entrada
    for i in range(len(listaEntradas)):
        for eachArchivo in archivosDeEntrada:
            if(listaEntradas[i] in eachArchivo):
                siEntradas[i] = True
                archivosEnOrden.append(eachArchivo)
                break
    # formar arreglo de condiciones
    siEntradas.append(cuatroPKLs)
    # fin de funcion
    return(all(siEntradas), archivosEnOrden)


# funcion: imprimir mensaje de avance ------------------------------------------
def imprimirAvance(porcetajeCaso):
    # variables locales
    tail = "".join(10*[" "])
    base = "-"
    term = "="
    pila = []
    terminado = ""
    porcetajeInt = 0
    barra = ""
    # hacer barra
    porcetajeInt = int(modf(porcetajeCaso/10)[1])
    for i in range(1, 11):
        if(i <= porcetajeInt):
            pila.append(term)
        else:
            pila.append(base)
    terminado = "".join(pila)
    barra = "0%  [" + terminado + "]  100%"
    # mensaje    
    print(barra + tail, end = "\r")
    # fin de funcion


# funcion: dibujar todas las graficas en una lista dada ------------------------
def dibujarGraficas(listaDeGraficas, nombreDeArchivo):
    # variables locales
    graficasPorHoja = 16
    factorCentrado = 15
    actual = 0             # contador de graficas para la iteracion del dibujado    
    G = None               # cada grafica
    nombreG6 = ""          # codificacion en G6 de la matriz de adyacencia
    orden = 0              # cantidad de vertices
    tamano = 0             # cantidad de aristas
    familia = ""           # solo "LA", solo "GA", "LAnGA", no amoeba "NO"
    vertices = dict()      # diccionario para nombrar vertice i como $v_{i+1}$    
    indice = ""  
    vertce = ""
    posiciones = None
    dibujoVertices = None
    leftX = 0
    rightX = 0
    topY = 0
    bottomY = 0
    nombreG6Str = ""
    nmStr = ""
    familiaStr = ""
    fig = None
    # crear pdf de varias hojas
    miPDF = matplotlib.backends.backend_pdf.PdfPages(nombreDeArchivo)
    while(actual < len(listaDeGraficas)):
        # definir dimensiones de pagina
        fig = plt.figure(figsize = (80, 80))
        for sub in range(1, graficasPorHoja + 1):
            # obtener datos de grafica actual
            (nombreG6, orden, tamano, familia) = listaDeGraficas[actual]
            # hacer subplot
            ax = fig.add_subplot(4, 4, sub)
            # crear grafica a partir de G6
            G = nx.from_graph6_bytes(nombreG6.encode())
            # reinicializar vertices
            vertices = dict()
            # hacer nombre de los vertices con formato latex
            for i in range(1, orden + 1):
                indice = "{" + str(i) + "}"
                vertice = "$v_{}$".format(indice)
                vertices[i - 1] = vertice
            # definir posiciones para los vertices
            if(nx.check_planarity(G, counterexample = False)[0]):
                posiciones = nx.planar_layout(G)
            else:
                posiciones = nx.spring_layout(G)
            # dibujar grafica
            nx.draw_networkx_nodes(G, pos = posiciones,
                                   edgecolors = "k", linewidths = 2,
                                   node_size = 1700, node_color = "w")
            nx.draw_networkx(G, pos = posiciones,
                             with_labels = True, labels = vertices,
                             width = 2.5, node_color = "w", font_size = 20)
            # centrar grafica en su margen
            leftX = min([a for [a, b] in list(posiciones.values())])
            rightX = max([a for [a, b] in list(posiciones.values())])
            topY = max([b for [a, b] in list(posiciones.values())])
            bottomY = min([b for [a, b] in list(posiciones.values())])
            plt.xlim(leftX + (leftX*factorCentrado/100), rightX + (rightX*factorCentrado/100))
            plt.ylim(bottomY + (bottomY*factorCentrado/100), topY + (topY*factorCentrado/100))
            # definir cadena de G6
            nombreG6Str = "g6: " + nombreG6
            # definir cadena de orden y tamano
            nmStr = "(n, m) = " + "(" + str(orden) + "," + str(tamano) + ")"            
            # definir cadena de familia
            if(familia == "LA"):
                familiaStr = "sólo LA"
            if(familia == "GA"):
                familiaStr = "sólo GA"
            if(familia == "LAnGA"):
                familiaStr = "LA$\cap$GA"
            if(familia == "NO"):
                familiaStr = "no amoeba"
            # agregar titulo            
            plt.title(nombreG6Str + "\n"
                      + nmStr + ",    " + familiaStr + ", " + "\n", fontsize = 28)
            # imprimir avance
            actual = actual + 1
            imprimirAvance(actual*100/len(listaDeGraficas))
            # concluir for si ya se alcanzo el limite
            if(actual == len(listaDeGraficas)):
                break
        # save figure
        miPDF.savefig(fig)
        plt.close()
    # guardar pdf con todas las hojas
    miPDF.close()
    # fin de funcion
            
            
# Main #########################################################################


# mensaje inicial
print("\n")
print(">>> Detect Amoebas within a Set of Arbitrary Graphs - Visualization - [@MarcosLaffitte - Github Repo - Amoebas]")


# revisar condiciones para continuar
(continuar, listaArchivos) = condicionesDeEntrada(archivos)


# detener programa si no se cumplen condiciones para continuar
if(not continuar):
    exit("> There is something wrong with the input files!\n\n")


# abrir los 4 archivos y vaciar datos en cuatro listas distintas
inFile = open(listaArchivos[0], "rb")
amoebasLA = pickle.load(inFile)                      
inFile.close() 
inFile = open(listaArchivos[1], "rb")
amoebasGA = pickle.load(inFile)                      
inFile.close() 
inFile = open(listaArchivos[2], "rb")
amoebasLAnGA = pickle.load(inFile)                      
inFile.close() 
inFile = open(listaArchivos[3], "rb")
graficasNoAmoeba = pickle.load(inFile)                      
inFile.close() 


# construir nombres de archivos de salida
amoebasLAFile = listaArchivos[0].split(".")[0] + ".pdf"
amoebasGAFile = listaArchivos[1].split(".")[0] + ".pdf"
amoebasLAnGAFile = listaArchivos[2].split(".")[0] + ".pdf"
graficasNoAmoebaFile = listaArchivos[3].split(".")[0] + ".pdf"


# dibujar LA
print("\n")
print("* Plotting Local-But-Not-Global Amoebas ...")
if(len(amoebasLA) == 0):
    print("- No graphs of this type were detected.")
else:
    print("- Tot. graphs of this type: " + str(len(amoebasLA)))
    dibujarGraficas(amoebasLA, amoebasLAFile)


# dibujar GA
print("\n")
print("* Plotting Global-But-Not-Local Amoebas ...")
if(len(amoebasGA) == 0):
    print("- No graphs of this type were detected.")    
else:
    print("- Tot. graphs of this type: " + str(len(amoebasGA)))
    dibujarGraficas(amoebasGA, amoebasGAFile)


# dibujar LAnGA
print("\n")
print("* Plotting Local-And-Global Amoebas ...")
if(len(amoebasLAnGA) == 0):
    print("- No graphs of this type were detected.")    
else:
    print("- Tot. graphs of this type: " + str(len(amoebasLAnGA)))
    dibujarGraficas(amoebasLAnGA, amoebasLAnGAFile)


# dibujar graficas No Amoeba
print("\n")
print("* Plotting Not-Amoeba Graphs ...")
if(len(graficasNoAmoeba) == 0):
    print("- No graphs of this type were detected.")    
else:
    print("- Tot. graphs of this type: " + str(len(graficasNoAmoeba)))
    dibujarGraficas(graficasNoAmoeba, graficasNoAmoebaFile)


# mensaje inicial
print("\n")
print(">>> Finished")
print("\n")


# Fin ##########################################################################
################################################################################
