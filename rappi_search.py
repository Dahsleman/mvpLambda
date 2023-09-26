from __future__ import print_function

from algorithms.aditional_queries_algorithm import AditionalQueriesAlgorithm as AQA
from google_sheet.google_sheet_api import GoogleSheetApi
from utils.rappi_product_utils import RappiProductUtils
from utils.file_generator import FileGenerator
from utils.rappi_utils import StringUtils
from input_settings import InputSettings
from node_code import NodeCode
from datetime import datetime
import subprocess
import geocoder 
import requests
import sys

search_dict = {}
new_products_list = {}
datetime_products_list = []
new_error_list = []
original_queries_dic = {}

def result():
  authorization = subprocess.run(['node', '-e', NodeCode.CODE], capture_output=True, text=True)
  return authorization

def storesList(lat, lng, query, bearer_token):
    stores_list = []
    # URL of the target endpoint
    url = 'https://services.rappi.com.br/api/pns-global-search-api/v1/unified-search?is_prime=false&unlimited_shipping=false'
    payload = {
        'lat': lat,
        'lng': lng,
        'query': query, 
        'options': {}
    }
    request_heathers = {
        'authorization' : bearer_token,
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36' 
    }
    
    try:
        response = requests.post(url, json=payload, headers=request_heathers)
        response.raise_for_status()
        if response.status_code == 200:
            json_data = response.json()
            stores = json_data['stores']
            for store in stores:
                stores_list.append(StringUtils.getStoreIdAndBrandName(store))
            return stores_list
        else:
            print('Request failed with status code, TRY AGAIN:', response.status_code)
            exit()
    
    except requests.exceptions.HTTPError as err:
        if response.status_code == 401:
            print('ERROR: NEED UPDATE TOKEN!!')
            exit()
        else:
            print('Request failed with status code, TRY AGAIN:', response.status_code)
            exit()
    except requests.exceptions.RequestException as err:
        print(f"REQUESTS ERROR, TRY AGAIN: {err}")
        exit()     

def geoAddress(address:str)->dict:
    g = geocoder.bing(address, key='Avs2Cjo6niYkuxjLApix0m6tplpt9qfz0SIgrW3_qoqGPZk62AsQCAxlraCz1oyV')
    results = g.json
    return results

def setupStoreList(_querys, _bearer_token, _search_dict):
    if len(_querys) != 0:
        for query, keyword in _querys.items():
            if keyword != "":
                term = query[0]
                unit = query[1]
                unit = unit.lower()
                if unit != "" and (unit == "kg" or unit == "gr" or unit == "l" or unit == "ml" or unit == "und"):
                    stores_list = storesList(results['lat'], results['lng'], term, _bearer_token)
                    query_list = list(query)
                    query_list[1] = unit
                    query = tuple(query_list)
                    print(query)
                    _search_dict[(query,keyword)] = stores_list
                else:
                    print(f'QUERY:{term}:{unit}')
                    print(f'Type diferent unit for {term}')
                    exit()
            else:
                print(f'Insert a keyword for: {query}')
                exit()       
        print('Querys OK')
    else:
        print('Input querys')
        exit()

def scrapeProducts(_search_dict, _new_products_list, _new_error_list):
    for _querys, _stores in _search_dict.items():
        keywords = _querys[1]
        query = _querys[0]
        term = query[0]
        unit = query[1]
        print(f'\rSCRAPING -- {term} -- PRODUCTS')
        if term.rfind(" ") != -1:
            term = term.replace(' ','%20')

        max_len_character = 0
        for i, store in enumerate(_stores):
            log_text = f'SCRAPING ({i + 1} / {len(_stores)}) - {store} STORE'
            if len(log_text) > max_len_character:
                max_len_character = len(log_text)
            print('{}'.format(log_text).ljust(max_len_character, ' '), end='\r')

            products_list, error_list = RappiProductUtils.scrapeProducts(store, term, unit, keywords, original_queries_dic)
            for product in products_list:
                product_id = product['product-id']
                if product_id not in _new_products_list.keys():
                    _new_products_list[product_id] = product
                elif product['k term-in-product-name?'] == 'True' and _new_products_list[product_id]['k term-in-product-name?'] == 'False':
                    _new_products_list[product_id] = product
            for error in error_list:
                if error['error'] != "":
                    _new_error_list.append(error)
        print("\r")     

"""INPUTS"""

# "bearer_token"
bearer_token = ""
clientDetails = InputSettings.CLIENTS[int(sys.argv[1])]
address = clientDetails["__ADDRESS__"]
client = clientDetails["__NAME__"]
querys = clientDetails["__QUERY__"]
AQA.addAditionalQueries(querys, original_queries_dic)

"""PROGRAM"""

if len(address) != 0:
    results = geoAddress(address)
    print('Adress OK')
else:
    print('Input an address')
    exit()
    
# Get the bearer_token
try:
    authorization = result()
    bearer_token = authorization.stdout.strip()
    print('Using generated Bearer_token')
except:
    if bearer_token:
        bearer_token
        print('Using default Bearer_token')
    else:
        print('Input bearer_token')
        exit()

# Setup the dictionary of the cities by query
setupStoreList(querys, bearer_token, search_dict)

print(f'SELECTED CLIENT: {client}')

# Starting scraping
current_datetime = datetime.now()
formatted_time = current_datetime.strftime("%Y-%m-%d | %H:%M:%S")
print(f'STARTING SCRAPING: {formatted_time}')
scrapeProducts(search_dict, new_products_list, new_error_list)
print("\r")

current_datetime = datetime.now()
formatted_time = current_datetime.strftime("%Y-%m-%d | %H:%M:%S")
print(f'SCRAPING ENDED: {formatted_time}')

#add datetime 
current_datetime = datetime.now()
formatted_datetime = current_datetime.strftime("%Y-%m-%d | %H:%M:%S")
for product in new_products_list.values():
    items = list(product.items())
    items.insert(0, ('k collected-at', formatted_datetime))
    product = RappiProductUtils.setupProductObjectWithHeader(dict(items))
    datetime_products_list.append(product)

print(f'TOTAL PRODUCTS SCRAPED: {len(datetime_products_list)}')

if len(datetime_products_list) > 0:
    FileGenerator.generateFiles(datetime_products_list, clientDetails, new_error_list)
    GoogleSheetApi.update_google_sheet(datetime_products_list, clientDetails, new_error_list)

current_datetime = datetime.now()
formatted_time = current_datetime.strftime("%Y-%m-%d | %H:%M:%S")
print(f'END SCRAPING: {formatted_time}')