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


import math
import config as cf
from DISClib.ADT.graph import gr
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.DataStructures import heap as h
from DISClib.Algorithms.Graphs import bfs as bf
from DISClib.Algorithms.Graphs import scc as scc
from DISClib.Algorithms.Graphs import dijsktra as Dk
from DISClib.Algorithms.Graphs import prim as pr
from DISClib.Algorithms.Graphs import dfs as df
from DISClib.ADT import stack as sk
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
                                     maptype='CHAINING',
                                    )
    catalog['Ciudades'] = mp.newMap(numelements=14000,
                                     maptype='CHAINING',
                                    )
    catalog['AirportsByIATA'] = mp.newMap(numelements=14000,
                                     maptype='CHAINING',
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
    UpdateAirlines(mapa,Aereolinia,origen,destino,distacia)

#CREACIÓN DE GRAFOS: DIRIGIDO Y NO DIRIGIDO 
def addConections(catalogo,origen,destino,distancia,GraphInD,GraphD,vuelo):
    edge = gr.getEdge(GraphD, origen, destino)
    if edge is None:
        PosbileNoDirigido = gr.getEdge(GraphD,destino,origen)
        if PosbileNoDirigido is not None:
            lt.addLast(catalogo["ElementosGraph"],vuelo)
            addVuelo(catalogo,GraphInD,origen)
            addVuelo(catalogo,GraphInD,destino)
            edge2 = gr.getEdge(GraphInD, origen, destino)
            if edge2 is None:
                gr.addEdge(GraphInD, origen, destino, distancia) 
        gr.addEdge(GraphD, origen, destino, distancia)
    return catalogo
def addVuelo(catalogo,Graph,Iata):
    if not gr.containsVertex(Graph, Iata):
        gr.insertVertex(Graph, Iata)
    return catalogo

#MAPA DE AEREOLINIAS CON SUS RESPECTIVOS VUELOS 

def UpdateAirlines(mapa,aereolinea,origen,destino,distancia):
    entry = mp.get(mapa,origen)
    if entry is None:
        lstVuelos = lt.newList(datastructure="ARRAY_LIST")
        vuelo = {"Aereolinea": aereolinea, "destino": destino,"Distancia": distancia}
        lt.addLast(lstVuelos,vuelo)
        mp.put(mapa,origen,lstVuelos)

    else:
        lstVuelos = entry["value"]
        vuelo = {"Aereolinea": aereolinea, "destino": destino,"Distancia": distancia}
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
def AereopuertosCercanos(ciudad1,ciudad2,catalogo):
    City1 = ciudad1["city"]
    lat1 = float(ciudad1["lat"])
    long1 = float(ciudad1["lng"])
    City2 = ciudad2["city"]
    lat2 = float(ciudad2["lat"])
    long2 = float(ciudad2["lng"])
    mapaAereopuertos = catalogo["AirportsBycity"]
    #Ciduad 1 
    MapaDistance1 = om.newMap(omaptype="RBT", comparefunction=compareElements)
    Aereopuertosbycity1 = mp.get(mapaAereopuertos,City1)["value"]
    for elemento in lt.iterator(Aereopuertosbycity1):
        lat = float(elemento["Latitude"])
        long = float(elemento["Longitude"])
        distance = calculoHaversine(lat1,long1,lat,long)
        om.put(MapaDistance1,distance,elemento)
    #Ciudad 2 
    MapaDistance2 = om.newMap(omaptype="RBT", comparefunction=compareElements)
    Aereopuertosbycity2 = mp.get(mapaAereopuertos,City2)["value"]
    for elemento2 in lt.iterator(Aereopuertosbycity2):
        lat3 = float(elemento2["Latitude"])
        long3 = float(elemento2["Longitude"])
        distance2 = calculoHaversine(lat2,long2,lat3,long3)
        om.put(MapaDistance2,distance2,elemento2)
    Aereopuerto1 = om.get(MapaDistance1, om.minKey(MapaDistance1))["value"]
    Aereopuerto2 = om.get(MapaDistance2, om.minKey(MapaDistance2))["value"]
    return Aereopuerto1, Aereopuerto2
def calculoHaversine(lat1,long1,lat2,long2):
    Radio = 6371e3
    Rlat1 = lat1 * math.pi/180
    Rlat2 = lat2 * math.pi/180
    DeltaLat = (lat2-lat1) * math.pi/180
    DeltaLong = (long2-long1) * math.pi/180
    a = math.sin(DeltaLat/2) * math.sin(DeltaLat/2) + math.cos(Rlat1) * math.cos(Rlat2) * math.sin(DeltaLong/2) * math.sin(DeltaLong/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = Radio * c
    return d 
def DijkstraReqcorrido(graph,aereo1,aereo2):
    Ruta = Dk.Dijkstra(graph,aereo1)
    camino = Dk.pathTo(Ruta,aereo2)
    return camino
def ArbolExpanciónMinima (cont, ciudad1):
    Cola = h.newHeap(cmpfunction=cmpmayorrecorrido)
    mapaNodirigido = cont['VuelosInDirec']
    ArbolRecubrimiento = pr.PrimMST(mapaNodirigido)
    arcos = pr.weightMST(mapaNodirigido,ArbolRecubrimiento)
    recorridodfs = df.DepthFirstSearch(mapaNodirigido,ciudad1)
    marked = lt.newList(datastructure="ARRAY_LIST")
    for vuelo in lt.iterator(ArbolRecubrimiento["mst"]):
        verticeA = vuelo["vertexA"]
        verticeB = vuelo["vertexB"]
        if verticeA != ciudad1:
            camino = df.pathTo(recorridodfs,verticeA)
            if camino != None and not lt.isPresent(marked,verticeA):
                lt.addLast(marked,verticeA)
                tamaño = lt.size(camino)
                info = {"Camino": camino, "peso": tamaño, "vertice": verticeA, "Weight": vuelo["weight"]}
                h.insert(Cola,info)
        if verticeB != ciudad1 and not lt.isPresent(marked,verticeB):
            camino2 = df.pathTo(recorridodfs,verticeB)
            if camino2 != None:
                lt.addLast(marked,verticeB)
                tamaño2 = lt.size(camino2)
                info2 = {"Camino": camino2, "peso": tamaño2, "vertice": verticeB}
                h.insert(Cola,info2)
    return arcos, Cola
def AfectedVertex(cont,codigo):
    marked = lt.newList(datastructure="ARRAY_LIST")
    # DATOS
    direct = cont["VuelosDirec"]
    Nodirect = cont["VuelosInDirec"]
    indegree = gr.indegree(direct,codigo)
    outdegree = gr.outdegree(direct,codigo)
    degreea = gr.degree(Nodirect,codigo)
    #CALCULOS   
    numafectados = outdegree
    #VERTICES
    adyacentesNoD = gr.adjacentEdges(Nodirect,codigo)
    adyacentesD = gr.adjacentEdges(direct,codigo)
    vertices = gr.vertices(direct)
    outdegrees = lt.newList(datastructure="ARRAY_LIST")
    for vertice in lt.iterator(vertices):
        if vertice != codigo:
            arco = gr.getEdge(direct,vertice,codigo)
            if arco is not None:
                 lt.addLast(outdegrees,arco)
    for indegree in lt.iterator(adyacentesD):
        verticeindegree = indegree["vertexB"]
        if not lt.isPresent(marked,verticeindegree):
            lt.addLast(marked, verticeindegree)
    for degreee in lt.iterator(adyacentesNoD):
        Vdegree = degreee["vertexB"]
        if not lt.isPresent(marked,Vdegree):
            lt.addLast(marked, Vdegree)
    for outdegree in lt.iterator(outdegrees):
        verticeDegree = outdegree["vertexB"]
        if not lt.isPresent(marked,verticeDegree):
            lt.addLast(marked, verticeDegree)
    return numafectados, marked
            






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
def compareElements (elemento1,elemento2):
    if (elemento1 == elemento2):
        return 0
    elif (elemento1 > elemento2):
        return 1
    else:
        return -1
def cmpmayorrecorrido(degree1,degree2):
    elemento1 = degree1["peso"]
    elemento2 = degree2["peso"]
    if elemento1 == elemento2:
        return 0
    elif elemento1 < elemento2:
        return 1
    else:
        return -1

# Funciones de ordenamiento
