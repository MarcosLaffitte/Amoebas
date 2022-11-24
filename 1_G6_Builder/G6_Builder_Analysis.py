################################################################################
#                                                                              #
#  README - Programa: G6_Builder_Analysis.py                                   #
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
#  - Descripcion: crea una lista de cadenas G6 que representan graficas        #
#    simples en dhico formato.                                                 #
#  - Input: Definido por el usuario dentro del programa. Se pueden agregar     #
#    cadenas G6 directamente, o bien crear graficas como listas de aristas.    #
#    El programa ya incluye ejemplos de todo esto mas abajo.                   #
#  - Output: un archivo de texto plano *.g6, con cadenas G6 cuyo nombre es     #
#    es determinado por el usuario mas abajo.                                  #
#  - Ejecutar como:                                                            #
#                   python3.7  G6_Builder_Analysis.py                          #
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
> Paquetes:  (instalados con anaconda)
***** networkx 2.5
***** sympy 1.7.1
"""


# Dependencias #################################################################


# instaladas con conda ---------------------------------------------------------
import networkx as nx


# Variables ####################################################################


# archivo de salida ------------------------------------------------------------
archivoG6 = "Thesis_Examples.g6"    # debe acabar con *.g6, ejempo "miArchivo.g6"


# archivo de salida ------------------------------------------------------------
someFile = None


# datos ------------------------------------------------------------------------
G = None
someBytes = None
someString = ""


# lista de cadenas G6 de las graficas ------------------------------------------
graficasG6 = []


# Main #########################################################################
# Graficas en G6, o que se convierten a G6, para agregarse a la lista graficasG6


# mensaje incial ---------------------------------------------------------------
print("\n")
print(">>> Builder of Graphs in G6 Format - [@MarcosLaffitte - Github Repo - Amoebas]")


# agregar P4 (con numeracion como en la tesis) ---------------------------------
G = nx.Graph()
G.add_edge(4, 1)
G.add_edge(1, 2)
G.add_edge(2, 3)
someBytes = nx.to_graph6_bytes(G, header = False)
someString = someBytes.decode()
graficasG6.append(someString)


# agregar ciclos C3, C4, C5, C6 y C7 -------------------------------------------
G = nx.Graph()
G.add_edge(1, 2)
G.add_edge(2, 3)
G.add_edge(3, 1)
someBytes = nx.to_graph6_bytes(G, header = False)
someString = someBytes.decode()
graficasG6.append(someString)
G = nx.Graph()
G.add_edge(1, 2)
G.add_edge(2, 3)
G.add_edge(3, 4)
G.add_edge(4, 1)
someBytes = nx.to_graph6_bytes(G, header = False)
someString = someBytes.decode()
graficasG6.append(someString)
G = nx.Graph()
G.add_edge(1, 2)
G.add_edge(2, 3)
G.add_edge(3, 4)
G.add_edge(4, 5)
G.add_edge(5, 1)
someBytes = nx.to_graph6_bytes(G, header = False)
someString = someBytes.decode()
graficasG6.append(someString)
G = nx.Graph()
G.add_edge(1, 2)
G.add_edge(2, 3)
G.add_edge(3, 4)
G.add_edge(4, 5)
G.add_edge(5, 6)
G.add_edge(6, 1)
someBytes = nx.to_graph6_bytes(G, header = False)
someString = someBytes.decode()
graficasG6.append(someString)
G = nx.Graph()
G.add_edge(1, 2)
G.add_edge(2, 3)
G.add_edge(3, 4)
G.add_edge(4, 5)
G.add_edge(5, 6)
G.add_edge(6, 7)
G.add_edge(7, 1)
someBytes = nx.to_graph6_bytes(G, header = False)
someString = someBytes.decode()
graficasG6.append(someString)


# Ejemplo de como agregar graficas en G6 - Grafica Rara no amoeba --------------
Gg6 = "G?Bev_"
Gg6 = Gg6 + "\n"
graficasG6.append(Gg6)


# Ejemplo de como agregar graficas en G6 - Amoeba Raras GA pero no LA ----------
Gg6 = "G?bBF_"
Gg6 = Gg6 + "\n"
graficasG6.append(Gg6)


# Minima grafica rara ----------------------------------------------------------
Gg6 = "EjsG"
Gg6 = Gg6 + "\n"
graficasG6.append(Gg6)


# locales no globales que dejan de ser amoebas al quitar reemplazos y GuK1'a ---
Gg6 = "G?`cmW"
GuK1 = nx.from_graph6_bytes(Gg6.encode())
Gg6 = Gg6 + "\n"
graficasG6.append(Gg6)
n = GuK1.order()
GuK1.add_node(n)
someBytes = nx.to_graph6_bytes(GuK1, header = False)
someString = someBytes.decode()
graficasG6.append(someString)
Gg6 = "HCQf@rK"
GuK1 = nx.from_graph6_bytes(Gg6.encode())
Gg6 = Gg6 + "\n"
graficasG6.append(Gg6)
n = GuK1.order()
GuK1.add_node(n)
someBytes = nx.to_graph6_bytes(GuK1, header = False)
someString = someBytes.decode()
graficasG6.append(someString)


# mas graficas que dejan de ser amoebas locales al quitar reemplazos raros -----
Gg6 = "G?qdrg"
Gg6 = Gg6 + "\n"
graficasG6.append(Gg6)
Gg6 = "G?qmrk"
Gg6 = Gg6 + "\n"
graficasG6.append(Gg6)
Gg6 = "GCpbvS"
Gg6 = Gg6 + "\n"
graficasG6.append(Gg6)
Gg6 = "H?ABCfE"
Gg6 = Gg6 + "\n"
graficasG6.append(Gg6)
Gg6 = "H?qadhi"
Gg6 = Gg6 + "\n"
graficasG6.append(Gg6)
Gg6 = "HCQbUgy"
Gg6 = Gg6 + "\n"
graficasG6.append(Gg6)


# C3 with short leg ------------------------------------------------------------
G = nx.Graph()
G.add_edge(1, 2)
G.add_edge(2, 3)
G.add_edge(3, 1)
G.add_edge(3, 4)
someBytes = nx.to_graph6_bytes(G, header = False)
someString = someBytes.decode()
graficasG6.append(someString)


# C3 with long leg --------------------------------------------------------------
G = nx.Graph()
G.add_edge(1, 2)
G.add_edge(2, 3)
G.add_edge(3, 1)
G.add_edge(3, 4)
G.add_edge(4, 5)
someBytes = nx.to_graph6_bytes(G, header = False)
someString = someBytes.decode()
graficasG6.append(someString)


# Cube Q3 ----------------------------------------------------------------------
G = nx.Graph()
G.add_edge(1, 2)
G.add_edge(2, 4)
G.add_edge(4, 3)
G.add_edge(3, 1)
G.add_edge(5, 6)
G.add_edge(6, 7)
G.add_edge(7, 8)
G.add_edge(8, 5)
G.add_edge(1, 5)
G.add_edge(2, 6)
G.add_edge(4, 7)
G.add_edge(3, 8)
someBytes = nx.to_graph6_bytes(G, header = False)
someString = someBytes.decode()
graficasG6.append(someString)


# P3 ---------------------------------------------------------------------------
G = nx.Graph()
G.add_edge(1, 2)
G.add_edge(1, 3)
someBytes = nx.to_graph6_bytes(G, header = False)
someString = someBytes.decode()
graficasG6.append(someString)


# K2 ---------------------------------------------------------------------------
G = nx.Graph()
G.add_edge(1, 2)
someBytes = nx.to_graph6_bytes(G, header = False)
someString = someBytes.decode()
graficasG6.append(someString)


# K4 ---------------------------------------------------------------------------
G = nx.Graph()
G.add_edge(1, 2)
G.add_edge(2, 3)
G.add_edge(3, 4)
G.add_edge(4, 1)
G.add_edge(1, 3)
G.add_edge(2, 4)
someBytes = nx.to_graph6_bytes(G, header = False)
someString = someBytes.decode()
graficasG6.append(someString)


# K2 u K2 ----------------------------------------------------------------------
G = nx.Graph()
G.add_edge(1, 4)
G.add_edge(2, 3)
someBytes = nx.to_graph6_bytes(G, header = False)
someString = someBytes.decode()
graficasG6.append(someString)


# K1,3 -------------------------------------------------------------------------
G = nx.Graph()
G.add_edge(4, 1)
G.add_edge(4, 2)
G.add_edge(4, 3)
someBytes = nx.to_graph6_bytes(G, header = False)
someString = someBytes.decode()
graficasG6.append(someString)


# Hexagon with triangle inside -------------------------------------------------
G = nx.Graph()
G.add_edge(1, 3)
G.add_edge(3, 5)
G.add_edge(5, 4)
G.add_edge(4, 2)
G.add_edge(2, 6)
G.add_edge(6, 1)
G.add_edge(1, 2)
G.add_edge(2, 3)
someBytes = nx.to_graph6_bytes(G, header = False)
someString = someBytes.decode()
graficasG6.append(someString)


# Weird triangle ---------------------------------------------------------------
G = nx.Graph()
G.add_edge(3, 7)
G.add_edge(7, 4)
G.add_edge(4, 3)
G.add_edge(4, 2)
G.add_edge(3, 6)
G.add_edge(3, 2)
G.add_edge(7, 6)
G.add_edge(4, 1)
G.add_edge(1, 5)
G.add_edge(2, 5)
G.add_edge(6, 5)
someBytes = nx.to_graph6_bytes(G, header = False)
someString = someBytes.decode()
graficasG6.append(someString)


# Two Adjacent Squares with leg ------------------------------------------------
G = nx.Graph()
G.add_edge(1, 5)
G.add_edge(5, 2)
G.add_edge(5, 4)
G.add_edge(4, 3)
G.add_edge(2, 3)
G.add_edge(3, 7)
G.add_edge(7, 6)
G.add_edge(6, 2)
someBytes = nx.to_graph6_bytes(G, header = False)
someString = someBytes.decode()
graficasG6.append(someString)


# Band of two rectangles and a square ------------------------------------------
G = nx.Graph()
G.add_edge(1, 2)
G.add_edge(1, 3)
G.add_edge(3, 5)
G.add_edge(2, 4)
G.add_edge(4, 6)
G.add_edge(5, 6)
G.add_edge(5, 7)
G.add_edge(7, 9)
G.add_edge(6, 8)
G.add_edge(8, 10)
G.add_edge(9, 10)
G.add_edge(9, 11)
G.add_edge(11, 12)
G.add_edge(10, 12)
G.add_edge(3, 7)
someBytes = nx.to_graph6_bytes(G, header = False)
someString = someBytes.decode()
graficasG6.append(someString)


# Minimo arbol global pero no local --------------------------------------------
G = nx.Graph()
G.add_edge(1, 2)
G.add_edge(2, 3)
G.add_edge(3, 4)
G.add_edge(5, 4)
G.add_edge(4, 6)
G.add_edge(6, 7)
G.add_edge(6, 8)
G.add_edge(8, 9)
G.add_edge(9, 10)
someBytes = nx.to_graph6_bytes(G, header = False)
someString = someBytes.decode()
graficasG6.append(someString)


# Minimas amoeba conexas globales pero no locales ------------------------------
G = nx.Graph()
G.add_edge(1, 2)
G.add_edge(2, 3)
G.add_edge(3, 4)
G.add_edge(4, 1)
G.add_edge(1, 5)
G.add_edge(4, 6)
someBytes = nx.to_graph6_bytes(G, header = False)
someString = someBytes.decode()
graficasG6.append(someString)

G = nx.Graph()
G.add_edge(1, 2)
G.add_edge(1, 3)
G.add_edge(1, 4)
G.add_edge(4, 5)
G.add_edge(5, 6)
G.add_edge(6, 4)
someBytes = nx.to_graph6_bytes(G, header = False)
someString = someBytes.decode()
graficasG6.append(someString)

G = nx.Graph()
G.add_edge(1, 2)
G.add_edge(2, 3)
G.add_edge(3, 4)
G.add_edge(4, 5)
G.add_edge(5, 6)
G.add_edge(6, 4)
someBytes = nx.to_graph6_bytes(G, header = False)
someString = someBytes.decode()
graficasG6.append(someString)

G = nx.Graph()
G.add_edge(1, 2)
G.add_edge(2, 3)
G.add_edge(2, 4)
G.add_edge(3, 5)
G.add_edge(5, 4)
G.add_edge(4, 6)
G.add_edge(6, 3)
someBytes = nx.to_graph6_bytes(G, header = False)
someString = someBytes.decode()
graficasG6.append(someString)


# Crear los primeros k = maxK arboles raros T^k de la familia infinita ---------
maxK = 3
for k in range(1, maxK + 1):
    # reinicializar G
    G = nx.Graph()    
    # vertices fijos
    G.add_nodes_from([1, 2, 3+6*k])    
    # trayectoria A1
    inicio = 3
    for i in range(k-1):
        G.add_edge(inicio + 6*i, inicio + 6*(i+1))
    # trayectoria A2
    inicio = 4
    for i in range(k-1):
        G.add_edge(inicio + 6*i, inicio + 6*(i+1))
    # trayectoria A3
    inicio = 5
    for i in range(k-1):
        G.add_edge(inicio + 6*i, inicio + 6*(i+1))
    # trayectoria A4
    inicio = 6
    for i in range(k-1):
        G.add_edge(inicio + 6*i, inicio + 6*(i+1))
    # trayectoria A5
    inicio = 7
    for i in range(k-1):
        G.add_edge(inicio + 6*i, inicio + 6*(i+1))
    # trayectoria A6
    inicio = 8
    for i in range(k-1):
        G.add_edge(inicio + 6*i, inicio + 6*(i+1))
    # 8 aristas uniendo las trayectorias
    G.add_edge(1, 5)
    G.add_edge(1, 4+6*(k-1))
    G.add_edge(1, 7+6*(k-1))
    G.add_edge(2, 5+6*(k-1))
    G.add_edge(2, 8+6*(k-1))
    G.add_edge(3+6*k, 4)
    G.add_edge(3+6*k, 3+6*(k-1))
    G.add_edge(3+6*k, 6+6*(k-1))
    # guardar grafica
    someBytes = nx.to_graph6_bytes(G, header = False)
    someString = someBytes.decode()
    graficasG6.append(someString)
    
    
# Ejemplo de graficas que son isomorfas pero tienen distinto G6 ----------------
Ga = nx.Graph()
Ga.add_edge(1, 2)
Ga.add_edge(2, 3)
Ga.add_edge(3, 4)
Ga.add_edge(4, 5)
Ga.add_edge(5, 6)
Ga.add_edge(6, 7)
Ga.add_edge(7, 1)
Ga.add_edge(1, 8)
Ga.add_edge(4, 9)
someBytes = nx.to_graph6_bytes(Ga, header = False)
someString = someBytes.decode()
graficasG6.append(someString)

Gb = nx.Graph()
Gb.add_edge(7, 5)
Gb.add_edge(5, 1)
Gb.add_edge(1, 4)
Gb.add_edge(4, 6)
Gb.add_edge(6, 3)
Gb.add_edge(3, 2)
Gb.add_edge(2, 7)
Gb.add_edge(1, 8)
Gb.add_edge(2, 9)
someBytes = nx.to_graph6_bytes(Gb, header = False)
someString = someBytes.decode()
graficasG6.append(someString)


# mensaje de impresion ---------------------------------------------------------
print("\n")
print("* Producing G6 File ...")


# Generar archivo con cadenas G6 -----------------------------------------------
someFile = open(archivoG6, "w")
someFile.writelines(graficasG6)
someFile.close()


# mensaje de termino -----------------------------------------------------------
print("\n")
print(">>> Finished")
print("\n")


# Fin ##########################################################################
################################################################################
