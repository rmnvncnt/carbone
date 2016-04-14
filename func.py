# -*- coding: latin-1 -*-

import requests, time, re, json, os
import pandas as pd

def get_product_infos(barcode):
    ''' return the product infos for a given barcode as json
    '''
    api_url = 'http://fr.openfoodfacts.org/api/v0/produit/'
    product_url = ''.join([api_url, str(barcode), '.json'])
    response = requests.get(product_url)
    json_data = response.json()
    return json_data['product']

def get_distance(product):
    ''' return the distance between user_location and
    production place for a given product
    '''
    usine_location = product['manufacturing_places_tags']
    product_origin = product['origins']
    user_location = 'Paris'
    # Google direction here?
    # Alternative : Geocoder + distance between points (worse)

def get_carbone_db(path):
    df = pd.read_csv(path, sep=';', encoding='latin-1') # read db
    df = df[df['Status'] == 'Valide'] # remove archived values

def get_emission(carbone_bd, product):
    pass
