################################################################################
#                                                                              #
#  README - Programa: 3_Reemplazos_Raros_Visualizacion.py                      #
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
#    3_Reemplazos_Raros_Analisis.py, y genera (a lo mas) cuatro archivos       #
#    con dibujos de todas las graficas dadas.                                  #
#  - Input:  4 archivos [Archivo*]_[Amoebas/Graficas]_[Raras/Ordinarias].pkl   #
#  - Output: cuatro archivos pdfs con los dibujos de las graficas dadas,       #
#            1) [Archivo*]_Amoebas_Raras.pdf        (LA, GA, LAnGA)            #
#            2) [Archivo*]_Graficas_Raras.pdf       (no amoebas)               #
#            3) [Archivo*]_Amoebas_Ordinarias.pdf   (LA, GA, LAnGA)            #
#            4) [Archivo*]_Graficas_Ordinarias.pdf  (no amoebas)               #
#  - Ejecutar como:                                                            #
#          python3.7  3_Reemplazos_Raros_Visualizacion.py  *.pkl               #
#                                                                              #
#  * en linea de comandos literalmente poner "*.pkl" y python toma todo *.pkl  #
#  * poniendo solo los 4 archivos *.pkl en la misma carpeta que este script.   #
#  * los 4 archivos *.pkl deben estar nombrados con el formato de Output de    #
#    3_Reemplazos_Raros_Analisis.py, de otra forma no se ejecuta el programa.  #
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
entrada1 = "Weird_Amoebas."
entrada2 = "Weird_Graphs."
entrada3 = "Ordinary_Amoebas."
entrada4 = "Ordinary_Graphs."
continuar = False
listaArchivos = []    # archivos en el orden de las entradas
amoebasRaras = []
graficasRaras = []
amoebasOrdinarias = []
graficasOrdinarias = []


# salida nombres de pdf's ------------------------------------------------------
amoebasRarasFile = ""
graficasRarasFile = ""
amoebasOrdinariasFile = ""
graficasOrdinariasFile = ""


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
    tipo = ""              # rara "R" u ordinaria "O"
    reemplazo = ()         # reemplazo admisible (r, s, k, l)
    listaReemps = []       # [[reemplazos ordinarios], [reemplazos raros]]
    reempsOrdinarios = []
    reempsRaros = []    
    leyendas = []          # leyenda para anotar reemplazos raros y ordinarios
    texto = ""             # textos en la leyenda
    extra = None           # atributos de leyenda
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
    tipoStr = ""
    fig = None
    # crear pdf de varias hojas
    miPDF = matplotlib.backends.backend_pdf.PdfPages(nombreDeArchivo)
    while(actual < len(listaDeGraficas)):
        # definir dimensiones de pagina
        fig = plt.figure(figsize = (80, 80))
        for sub in range(1, graficasPorHoja + 1):
            # obtener datos de grafica actual
            (nombreG6, orden, tamano, familia, tipo, listaReemps) = listaDeGraficas[actual]
            reempsOrdinarios = listaReemps[0]
            reempsRaros = listaReemps[1]
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
            # reinicializar leyendas
            leyendas = ["Reemplazos" + "\n" + "No Triviales" + "\n"]
            # hacer leyenda para reemplazos raros
            if(len(reempsRaros) == 0):
                leyendas.append("Raros")
                leyendas.append("(no hay)")                
            else:
                leyendas.append("Raros")
                for (r, s, k, l) in reempsRaros:
                    texto = str(r + 1) + " " + str(s + 1) + r"$\rightarrow$" + str(k + 1) + " " + str(l + 1)
                    leyendas.append(texto)
            # espacio entre leyendas
            leyendas.append("\n")  
            # hacer leyenda para reemplazos ordinarios
            if(len(reempsOrdinarios) == 0):
                leyendas.append("Ordinarios") 
                leyendas.append("(no hay)")               
            else:
                leyendas.append("Ordinarios")
                for (r, s, k, l) in reempsOrdinarios:
                    texto = str(r + 1) + " " + str(s + 1) + r"$\rightarrow$" + str(k + 1) + " " + str(l + 1)
                    leyendas.append(texto)            
            # atributos de leyenda
            extra = Rectangle((0, 0), 0, 0, fc = "w", fill = False, edgecolor = "none", linewidth = 0)
            ax.legend([extra]*len(leyendas), leyendas, fontsize = 15, framealpha = 1,
                      loc = "upper right", handlelength = 0, handletextpad = 0,
                      bbox_to_anchor = (1.13, 1.01))
            # definir posiciones para los vertices
            if(nx.check_planarity(G, counterexample = False)[0]):
                posiciones = nx.planar_layout(G)
            else:
                posiciones = nx.spring_layout(G)
            # dibujar grafica
            nx.draw_networkx_nodes(G, pos = posiciones,
                                   edgecolors = "k", linewidths = 2,
                                   node_size = 1500, node_color = "w")
            nx.draw_networkx(G, pos = posiciones,
                             with_labels = True, labels = vertices,
                             width = 2.5, node_color = "w", font_size = 18)
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
            # definir cadena de tipo
            if(tipo == "O"):
                tipoStr = "Ordinaria"
            if(tipo == "R"):
                tipoStr = "Rara"
            # agregar titulo            
            plt.title(nombreG6Str + "\n" + nmStr + ", " + familiaStr + ", " + tipoStr, fontsize = 18)
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
print(">>> Weird Edge-Replacements - Visualization - [@MarcosLaffitte - Github Repo - Amoebas]")


# revisar condiciones para continuar
(continuar, listaArchivos) = condicionesDeEntrada(archivos)


# detener programa si no se cumplen condiciones para continuar
if(not continuar):
    exit("> There is something wrong with the input files!\n\n")


# abrir los 4 archivos y vaciar datos en cuatro listas distintas
inFile = open(listaArchivos[0], "rb")
amoebasRaras = pickle.load(inFile)                      
inFile.close() 
inFile = open(listaArchivos[1], "rb")
graficasRaras = pickle.load(inFile)                      
inFile.close() 
inFile = open(listaArchivos[2], "rb")
amoebasOrdinarias = pickle.load(inFile)                      
inFile.close() 
inFile = open(listaArchivos[3], "rb")
graficasOrdinarias = pickle.load(inFile)                      
inFile.close() 


# construir nombres de archivos de salida
amoebasRarasFile = listaArchivos[0].split(".")[0] + ".pdf"
graficasRarasFile = listaArchivos[1].split(".")[0] + ".pdf"
amoebasOrdinariasFile = listaArchivos[2].split(".")[0] + ".pdf"
graficasOrdinariasFile = listaArchivos[3].split(".")[0] + ".pdf"


# dibujar amoebas raras
print("\n")
print("* Plotting Weird Amoebas ...")
if(len(amoebasRaras) == 0):
    print("- No amoebas of this type were detected.")
else:
    print("- Tot. graphs of this type: " + str(len(amoebasRaras)))
    dibujarGraficas(amoebasRaras, amoebasRarasFile)


# dibujar graficas raras
print("\n")
print("* Plotting Weird Graphs (Not Amoeba) ...")
if(len(graficasRaras) == 0):
    print("- No graphs of this type were detected.")
else:
    print("- Tot. graphs of this type: " + str(len(graficasRaras)))
    dibujarGraficas(graficasRaras, graficasRarasFile)


# dibujar amoebas ordinarias
print("\n")
print("* Plotting Ordinary Amoebas ...")
if(len(amoebasOrdinarias) == 0):
    print("- No graphs of this type were detected.")
else:
    print("- Tot. graphs of this type: " + str(len(amoebasOrdinarias)))
    dibujarGraficas(amoebasOrdinarias, amoebasOrdinariasFile)


# dibujar graficas ordinarias
print("\n")
print("* Plotting Ordinary Graphs (Not Amoeba) ...")
if(len(graficasOrdinarias) == 0):
    print("- No graphs of this type were detected.")    
else:
    print("- Tot. graphs of this type: " + str(len(graficasOrdinarias)))
    dibujarGraficas(graficasOrdinarias, graficasOrdinariasFile)


# mensaje inicial
print("\n")
print(">>> Finished")
print("\n")


# Fin ##########################################################################
################################################################################
