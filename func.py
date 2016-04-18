# -*- coding: latin-1 -*-

from geopy.geocoders import Nominatim
from geopy.distance import vincenty
from unidecode import unidecode

import requests, json, re
import pandas as pd

def get_product_infos(barcode):
    ''' return the product infos for a given barcode as json
    out: dict (json)
    '''
    api_url = 'http://fr.openfoodfacts.org/api/v0/produit/'
    product_url = ''.join([api_url, str(barcode), '.json'])
    response = requests.get(product_url)
    json_data = response.json()['product']
    return json_data

def get_distance_infos(product, uloc='Paris'):
    ''' get the shortest distance between production location
    and user location (default = Paris)
    out: float
    '''
    # get product origins
    # from the most accurate to the least
    if product['manufacturing_places_tags']:
        places = product['manufacturing_places_tags']
    elif product['origins']:
        places = product['origins']
    else:
        places = product['countries']

    # str to list
    if isinstance(places, str):
        places = [places]

    # get geolocation
    geolocator = Nominatim()
    locations = [geolocator.geocode(p) for p in places if p]
    ucoord = geolocator.geocode(uloc)

    # get distances
    distances = []
    for floc in locations:
        distance = vincenty((ucoord.latitude, ucoord.longitude),
                            (floc.latitude, floc.longitude)).kilometers
        distances.append(distance)

    # return shortest distance
    distance = min(distances)
    return distance, places

def get_db(path):
    ''' read carbon emission factor data base
    out : pandas DataFrame
    '''
    # read db
    df = pd.read_csv(path, sep=';', encoding='latin-1')
    # unicode to ascii
    df.columns = [unidecode(x) for x in df.columns]
    df = df.applymap(lambda x: unidecode(x) if isinstance(x, str) else x)
    # clean archived entries
    df = df[df["Statut de l'element"] == "Valide generique"]
    # get emission factors only
    df = df[df["Type de l'element"] == "Facteur d'emission"]
    return df

def get_emission(carbone_bd, product):
    pass

def get_ingredients_list(product):
    ''' read the ingredients of the product only when proportion is given from OFF '''
    # get the weight of the product and unite
    total_weight = int(re.findall(r'\d+', product['quantity'])[0])
    unite = re.findall(r'[a-zA-Z]', product['quantity'])[0]
    # get ingredient_list
    ingredient_list = product['ingredients_text']
    #clean sub composition
    ingredient_list_clean = re.sub('\[.*?\]','', ingredient_list)
    #get ingredients with proportion only
    return [ingredient for ingredient in ingredient_list_clean.split(', ') if any(j.isdigit() for j in ingredient)]
    #match ingredient_name and ingredient_percent
