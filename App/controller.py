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
 """

import config as cf
import model
import csv


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo
def init():
    catalogo = model.newcatalog()
    return catalogo
# Funciones para la carga de datos
def LoadInfo(catalogo,rutas,worldcities,airports):
    airports = LoadAirports(catalogo,airports)
    rutas = LoadRutas(catalogo,rutas)
    cities = LoadCities(catalogo,worldcities)
    primerosYulti = {"Rutas": rutas, "Airports": airports, "cities": cities}
    return primerosYulti
def LoadRutas(catalago,archivo):
    archivo = cf.data_dir + archivo
    input_file = csv.DictReader(open(archivo, encoding="utf-8"),
                                delimiter=",")
    firstFile = None
    lastFile = None
    for ruta in input_file:
        if firstFile == None:
            firstFile = ruta
        model.addAirportsConections(catalago,ruta)
        lastFile = ruta
    return firstFile, lastFile
        
def LoadAirports(catalago,archivo):
    firstFile = None
    lastFile = None
    archivo = cf.data_dir + archivo
    input_file = csv.DictReader(open(archivo, encoding="utf-8"),
                                delimiter=",")
    for airport in input_file:
        if firstFile == None:
            firstFile = airport
        model.addAirportsbycity(catalago,airport)
        lastFile = airport
    return firstFile, lastFile
def LoadCities(catalago,archivo):
    firstFile = None
    lastFile = None
    archivo = cf.data_dir + archivo
    input_file = csv.DictReader(open(archivo, encoding="utf-8"),
                                delimiter=",")
    for citie in input_file:
        if firstFile == None:
            firstFile = citie
        model.addCities(catalago,citie)
        lastFile = citie      
    return firstFile, lastFile

# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo
def totalfligths(cont,graph):
   
    return model.totalfligths(cont,graph)


def totalConnections(cont,graph):
   
    return model.totalConnections(cont,graph)
def maxconections(graph):
    return model.maxoutdigree(graph)
def ComponentesConectados(graph,a1,a2):
    return model.SCC (graph,a1,a2)
def BuscarHomonimos(catalogo,ciudad1,ciudad2):
    return model.BuscarHomonimos(catalogo,ciudad1,ciudad2)
