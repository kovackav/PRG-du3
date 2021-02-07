import json, os
from math import sqrt
from geojson import FeatureCollection, dump

path_trasy = "trasy.geojson"
lenhran = 50

def load_file(path):
    '''Nacteni vstupniho souboru. Pokud soubor chybi (spatne zadana cesta), vyskoci chyba.'''
    try:
        with open(path, encoding="UTF-8") as json_file:
            return json.load(json_file)["features"]
    except ValueError: 
        print(f"Soubor {path} neni validni GeoJSON.")
        exit()
    except FileNotFoundError:
        print(f"Vstupni data {path} se nepodarilo nalezt, zkontrolujte cestu.")
        exit()
    except PermissionError:
        print(f"Vstupni data {path} existuji, ale program k nim nema pristup.")
        exit()


def pythagor(x, y):
    '''Pythagorova veta.'''
    return sqrt((x[0] - y[0])**2 + (x[1] - y[1])**2)

def novybod(x, y):
    '''Vypocet souradnic noveho bodu, pokud je segment prilis dlouhy.'''
    return (x[0] - y[0])/2 + y[0] , (x[1] - y[1])/2 + y[1] 

json_trasy = load_file(path_trasy)

for feature in json_trasy:
        coor = feature["geometry"]["coordinates"]
        lencoor = len(coor)
        for i in range (lencoor-1):
            lenseg = pythagor(coor[i],coor[i+1])
            if lenseg > lenhran:
                coor_novybod = novybod(coor[i],coor[i+1])
                feature['geometry']['coordinates'].append(coor_novybod)

feature_collection = FeatureCollection(json_trasy)

with open('output.geojson', 'w') as f:
   dump(feature_collection, f, indent=3)


                

