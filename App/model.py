"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
from DISClib.ADT.graph import gr, indegree
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.DataStructures import heap as h
from DISClib.Algorithms.Graphs import bfs as bf
from DISClib.Algorithms.Graphs import scc as scc
assert cf
import time
def newcatalog():
    catalog = {
            'Airlines': None,
            'Airports': None,
            'Vuelos': None,
            'components': None,
            'paths': None}
    catalog['Airlines'] = mp.newMap(numelements=14000,
                                     maptype='PROBING',
                                    )

    catalog['VuelosDirec'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True,
                                              size=14000,
                                              comparefunction=compareStopIds
                                              )
    catalog['VuelosInDirec'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=False,
                                              size=14000,
                                              comparefunction=compareStopIds
                                             )
    catalog['AirportsBycity'] = mp.newMap(numelements=14000,
                                     maptype='CHANING',
                                    )
    catalog['Ciudades'] = mp.newMap(numelements=14000,
                                     maptype='CHANING',
                                    )
    catalog['AirportsByIATA'] = mp.newMap(numelements=14000,
                                     maptype='CHANING',
                                    )
    catalog["ElementosGraph"] = lt.newList(datastructure="ARRAY_LIST")
    return catalog  


# Construccion de modelos

# Funciones para agregar informacion al catalogo
def addAirportsbycity(catalog,airport):
    ciudad = airport["City"]
    mapa = catalog["AirportsBycity"]
    Iata = airport["IATA"]
    mapaI = catalog["AirportsByIATA"]
    GraphD = catalog["VuelosDirec"]
    addVuelo(catalog,GraphD,Iata)
    UpdateAirpotsbyCity(airport, ciudad, mapa)
    UpdateAirports(mapaI,Iata,airport)

def UpdateAirpotsbyCity(airport, ciudad, mapa):
    entry = mp.get(mapa,ciudad)
    if entry is None:
        lstVuelos = lt.newList(datastructure="ARRAY_LIST")
        lt.addLast(lstVuelos,airport)
        mp.put(mapa,ciudad,lstVuelos)

    else:
        lstVuelos = entry["value"]
        lt.addLast(lstVuelos,airport)

def addCities(catalog,ciudad):
    ciudadAguardar = ciudad["city"]
    mapa = catalog["Ciudades"]
    entry = mp.get(mapa,ciudadAguardar)
    if entry is None:
        lstVuelos = lt.newList(datastructure="ARRAY_LIST")
        lt.addLast(lstVuelos,ciudad)
        mp.put(mapa,ciudadAguardar,lstVuelos)

    else:
        lstVuelos = entry["value"]
        lt.addLast(lstVuelos,ciudad)
        
def addAirportsConections(catalog,vuelo):
    origen = vuelo["Departure"]
    destino = vuelo["Destination"]
    distacia = float(vuelo["distance_km"])
    Aereolinia = vuelo["Airline"]
    mapa = catalog["Airlines"]
    GraphD = catalog["VuelosDirec"]
    GraphInD = catalog["VuelosInDirec"]
    addConections(catalog,origen,destino,distacia,GraphInD,GraphD,vuelo)
    UpdateAirlines(mapa,Aereolinia,origen,destino)

#CREACIÓN DE GRAFOS: DIRIGIDO Y NO DIRIGIDO 
def addConections(catalogo,origen,destino,distancia,GraphInD,GraphD,vuelo):
    edge = gr.getEdge(GraphD, origen, destino)
    if edge is None:
        gr.addEdge(GraphD, origen, destino, distancia)
    else:
        lt.addLast(catalogo["ElementosGraph"],vuelo)
        addVuelo(catalogo,GraphInD,origen)
        addVuelo(catalogo,GraphInD,destino)
        edge2 = gr.getEdge(GraphInD, origen, destino)
        if edge2 is None:
            gr.addEdge(GraphInD, origen, destino, distancia) 
    return catalogo
def addVuelo(catalogo,Graph,Iata):
    if not gr.containsVertex(Graph, Iata):
        gr.insertVertex(Graph, Iata)
    return catalogo

#MAPA DE AEREOLINIAS CON SUS RESPECTIVOS VUELOS 

def UpdateAirlines(mapa,aereolinea,origen,destino):
    entry = mp.get(mapa,aereolinea)
    if entry is None:
        lstVuelos = lt.newList(datastructure="ARRAY_LIST")
        vuelo = {"origen": origen, "destino": destino}
        lt.addLast(lstVuelos,vuelo)
        mp.put(mapa,aereolinea,lstVuelos)

    else:
        lstVuelos = entry["value"]
        vuelo = {"origen": origen, "destino": destino}
        lt.addLast(lstVuelos,vuelo)
def UpdateAirports(mapa,IATA,info):
    entry = mp.get(mapa,IATA)
    if entry is None:
        mp.put(mapa,IATA,info)






# Funciones para creacion de datos

# Funciones de consulta
def totalfligths(analyzer,graph):
    
    return gr.numVertices(graph)


def totalConnections(analyzer,graph):
    
    return gr.numEdges(graph)



def maxoutdigree(graph):
    cola = h.newHeap(cmpfunction=cmpmayordegree)
    MapVértices = gr.vertices(graph)
    conectedComponents = 0
    for vertice in lt.iterator(MapVértices):
        outdigree = gr.outdegree(graph,vertice)
        indegree = gr.indegree(graph,vertice)
        if indegree != 0 or outdigree != 0:
            conectedComponents += 1 
        info = {"Conections": outdigree + indegree , "Outdegree": outdigree, "Indegree": indegree, "Vertice": vertice}
        h.insert(cola,info)
    return cola,conectedComponents
def SCC(graph,A1,A2):
    Scc = scc.KosarajuSCC(graph)
    componentesConectados = Scc["components"]
    Idconected1 = mp.get(Scc["idscc"],A1)["value"]
    Idconected2 = mp.get(Scc["idscc"],A2)["value"]
    existencia = False
    if Idconected1 == Idconected2:
        existencia = True
    return existencia,componentesConectados
def BuscarHomonimos(catalogo,ciudad1,ciudad2):
    mapaCiudades = catalogo["Ciudades"]
    homonimos1 = mp.get(mapaCiudades,ciudad1)["value"]
    homonimos2 = mp.get(mapaCiudades,ciudad2)["value"]
    return homonimos1, homonimos2



# Funciones utilizadas para comparar elementos dentro de una lista
def compareStopIds(stop, keyvaluestop):
    stopcode = keyvaluestop['key']
    if (stop == stopcode):
        return 0
    elif (stop > stopcode):
        return 1
    else:
        return -1
def cmpmayordegree(degree1,degree2):
    elemento1 = degree1["Conections"]
    elemento2 = degree2["Conections"]
    if elemento1 == elemento2:
        return 0
    elif elemento1 < elemento2:
        return 1
    else:
        return -1

# Funciones de ordenamiento
