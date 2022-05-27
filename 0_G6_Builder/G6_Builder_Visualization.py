################################################################################
#                                                                              #
#  README - Programa: 0_Creador_G6_Visualizacion.py                            #
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
#  - Descripcion: recibe una lista de graficas en formato G6 y regresa         #
#    un pdf con los dibujos de todas las graficas dadas.                       #
#  - Input: archivo con terminacion *.g6, es decir [archivo*].g6               #
#  - Output: pdf con dibujos de las graficas, con un total de graficas         #
#    definido por el usuario mas abajo. Default 1600 graficas.                 #
#  - Ejecutar como:                                                            #
#         python3.7  0_Creador_G6_Visualizacion.py  [archivo*].g6              #
#                                                                              #
#  - Fecha: 22 de abril 2022                                                   #
#                                                                              #
#  * las variables se nombran con formato estilo java                          #
#  * la enumaracion de los vertices puede cambiar debido a las conversiones    #
#    entre G6 y listas de aristas.                                             #
#                                                                              #
################################################################################


# Requiere #####################################################################


"""
> Lenguaje: python 3.7
> Anaconda: 4-bit version - conda 4.10.1
> Paquetes:
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
from sys import argv
from math import modf


# apagar warnings y matplotlib en backend para correr en servidor --------------
import warnings
matplotlib.use("Agg")
warnings.filterwarnings("ignore")


# Variables ####################################################################


# nombre del archivo de salida -------------------------------------------------
graficasFile = "Thesis_Examples.pdf"


# limite de graficas a dibujar definido por el usuario -------------------------
# totDibujar = 1600   (default: 16 por hoja x 100 hojas)
totDibujar = 1600


# recipientes de datos ---------------------------------------------------------
inFile = None
archivog6 = argv[1]
graficas = []


# Funciones ####################################################################


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
    fig = None
    # crear pdf de varias hojas
    miPDF = matplotlib.backends.backend_pdf.PdfPages(nombreDeArchivo)
    while(actual < len(listaDeGraficas)):
        # definir dimensiones de pagina
        fig = plt.figure(figsize = (80, 80))
        for sub in range(1, graficasPorHoja + 1):
            # obtener nombre G6 de grafica actual
            nombreG6 = listaDeGraficas[actual]
            # hacer subplot
            ax = fig.add_subplot(4, 4, sub)
            # crear grafica a partir de G6 y obtener orden y tamano
            G = nx.from_graph6_bytes(nombreG6.encode())
            orden = G.order()
            tamano = G.size()
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
                                   node_size = 1750, node_color = "w")
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
            # agregar titulo            
            plt.title(nombreG6Str + "\n" + nmStr, fontsize = 18)
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


# mensaje incial
print("\n")
print(">>> Visualization of Graphs in G6 Format  - [@MarcosLaffitte - Github Repo - Amoebas]")


# abrir archivo
inFile = open(archivog6, "r")
graficas = inFile.readlines()                      
inFile.close()


# limpiar salto de linea en cada g6
graficas = [eachGraph.rstrip("\n") for eachGraph in graficas]


# mensaje de impresion
print("\n")
print("* Plotting Graphs ...")


# elegir una cantidad de graficas a dibujar
if(len(graficas) >= totDibujar):
    dibujarGraficas(graficas[:totDibujar], graficasFile)
else:
    dibujarGraficas(graficas, graficasFile)


# mensaje de termino
print("\n")
print("\n")
print(">>> Finished")
print("\n")
    

# Fin ##########################################################################
################################################################################
