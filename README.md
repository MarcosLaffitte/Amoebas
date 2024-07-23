# Welcome to the Repo

<p align="center">
<img src="./7_Readme_Pics/C3.gif" width="180"/><img src="./7_Readme_Pics/RepoTitle.png" width="300"/><img src="./7_Readme_Pics/P4.gif" width="180"/>
</p>


## Developed by

- Mtr. Marcos E. González Laffitte<br/>
  IMATE - UNAM Campus Juriquilla, México.<br/>
  marcoslaffitte@gmail.com

- Dra. Amanda Montejano Cantoral<br/>
  UMDI - Facultad de Ciencias - UNAM Campus Juriquila, México<br/>
  amandamontejano@ciencias.unam.mx


## About

<p align="justify">
Amoebas are a family of simple graphs first defined by Adriana Hansberg, Yair Caro and Amanda Montejano, who initially studied them in the context of Ramsey-Turán Theory [1, 2]. The study of these graphs is of interest, in particular, due to its relation with the graph isomorphism problem. All the programs here can be used to detect amoebas and analyze their properties. This repository was developed as part of the work of Marcos E. González Laffitte's Master Thesis in Mathematics [3] under supervision of Dra. Amanda Montejano Cantoral.<br/>
</p>


## Description

<p align="justify">
   Here we provide two different implementations of the same algorithm. If you wish to analyze only one graph, you can make use of the script Amoebas_Standalone.py in this repository. You can find the instructions on how to use this below. On the other hand, if you want to analyze a big batch of graphs you would need to use the scripts in the other folders. For instructions on this keep reading this section.
</p>

<p align="justify">
All the directories / folders numbered from 1 to 5 contain each two Python scripts that can be used to detect and analyze different properties of amoebas, as shown in the Instruction_Manual.pdf included in this repository (please find below a direct link to it). On the other hand, the folder 6_Examples contains the results of three different analyses: one over the set of graphs named Thesis_Examples.g6, other over the set of all non-isomorphic graphs having from 1 and up to 7 vertices, and finally a collection of the results obtained for bigger sets of graphs, specifically over all the non-isomorphic graphs having from 1 and up to 10 vertices, as well as over all the non-isomorphic trees having from 1 and up to 22 vertices. Please take into account that some of these last pdf files are large, and therefore should be downloaded in order to be visualized properly.<br/>
</p>

> Please find <a href="./Instruction_Manual.pdf">here</a> the detailed instruction manual for the programs in this repo.<br/>


## Cite as

This repository was also developed as part of the contribution:

**[1]**   Marcos E. González Laffitte, J. René González-Martínez, Amanda Montejano, On the detection of local and global amoebas: theoretical insights and practical algorithms (Brief Announcement). *Procedia Computer Science* **223** (2023) pp. 376-378.
> **Link:** https://doi.org/10.1016/j.procs.2023.08.252

<div align="justify">
This work was developed for research purposes. Please cite as above if you find this work or these programs useful for your own research.
</div>
<br/>


## Instructions for the Stand-alone script

###### In order to run the script Amoebas_Standalone.py you will require some python packages. You can install them directly into a new anaconda environment as follows:

```
conda create -n amoebas networkx matplotlib sympy
```
###### Then activate the amoebas conda environment:
```
conda activate amoebas
```
###### And execute the program with:
```
python  Amoebas_Standalone.py
```

###### Remember to always activate the amoebas conda environment before using this script.

###### The input graph can be modified IN-CODE, i.e., inside the script. This is done in this way since determining a whole graph depends heavily on each user's data-representation. The graph can be built in the script as a NetworkX object [8] by specifying its edges. The script will produce a PDF with a plot of the graph stating if it is indeed an amoeba and its type (local and/or global), or if it is not an amoeba.

###### IMPORTANT: the other scripts in the repository require the Sage Math for python, which you have to install through Anaconda: https://doc.sagemath.org/html/en/installation/conda.html. Nonetheless Amoebas_Standalone.py only requires the packages in the environment as installed above.


## References

#### Literature

[1] Yair Caro, Adriana Hansberg, Amanda Montejano, "Graphs isomorphisms under edge-replacements and the family of amoebas", p. 33, 2021.<br/>
https://doi.org/10.48550/arXiv.2007.11769

[2] Yair Caro, Adriana Hansberg, Amanda Montejano, "Unavoidable chromatic patterns in 2-colorings of the complete graph". Journal of Graph Theory, 2021, vol. 97, pages 123-147.<br/>
https://onlinelibrary.wiley.com/doi/abs/10.1002/jgt.22645

[3] Marcos Emmanuel González Laffitte, Tesis de Maestría en Ciencias Matemáticas, UNAM, "Estudio de Amoebas y sus Propiedades: Detección Computacional de esta Familia de Gráficas y el Caso de los Reemplazos Raros", p. 111, 2022. Complete text Available in Spanish at: <br/>
http://132.248.9.195/ptd2022/septiembre/0831065/Index.html


#### Used Database of Graphs and Trees - Last visited on: June 10th, 2022

[4] Main page: Combinatorial Data - Prof. Brendan D. McKay, School of Computing, Australian National University.<br/>
https://users.cecs.anu.edu.au/~bdm/data/

[5] Simple Graphs having from 1 and up to 10 vertices were obtained from: Graphs Page - Prof. Brendan D. McKay, School of Computing, Australian National University.<br/>
https://users.cecs.anu.edu.au/~bdm/data/graphs.html

[6] Trees having from 1 and up to 22 vertices were obtained from: Trees Page - Prof. Brendan D. McKay, School of Computing, Australian National University.<br/>
https://users.cecs.anu.edu.au/~bdm/data/trees.html

[7] Definition of graph6 encoding - Prof. Brendan D. McKay, School of Computing, Australian National University.<br/>
https://users.cecs.anu.edu.au/~bdm/data/formats.txt


#### NetworkX - Last visited on: July 23th, 2024
[8] https://networkx.org/