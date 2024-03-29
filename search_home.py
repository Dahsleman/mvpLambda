from __future__ import print_function

from algorithms.aditional_queries_algorithm import AditionalQueriesAlgorithm as AQA
from utils.product_formatter_utils import ProductFormatter, JsonFile
from google_sheet.google_sheet_api import GoogleSheetApi
from utils.rappi_utils import StringUtils, Playwright
from utils.file_generator import FileGenerator
from input_settings import InputSettings
from utils.xlsx_utils import XlsxUtils
from datetime import datetime
import geocoder 
import requests
import asyncio
import sys
import os   

def setProductsJson(_products_list:list, address=None, term=None, product_name=None):
    if address == None:
        
        directory_path = "./data/json/mvp"
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)
            print(f"The folder {directory_path} was created.")

        formatted_address = JsonFile.format_str(address)
        json_file_name = f'{directory_path}/{term}_{formatted_address}'
        JsonFile.createJsonFile(_products_list, json_file_name)

    elif term == None:
        _new_products_list = []
        _products_dict = {}
        _products_dict['status'] = 200
        _products_dict['product_formatted_name'] = product_name
        _products_dict['search_details_results_count'] = len(_products_list)
        _products_dict['search_details_results'] = _products_list
        _new_products_list.append(_products_dict)

        directory_path = "./data/json/search_details"
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)
            print(f"The folder {directory_path} was created.")

        formatted_name = JsonFile.format_str(product_name)
        formatted_address = JsonFile.format_str(address)
        json_file_name = f'{directory_path}/{formatted_name}_{formatted_address}'
        JsonFile.createJsonFile(_new_products_list, json_file_name)

    elif product_name == None:
        _new_products_list = []
        _products_dict = {}
        _products_dict['status'] = 200
        _products_dict['search_home_results_count'] = len(_products_list)
        _products_dict['search_home_results'] = _products_list
        _new_products_list.append(_products_dict)
        
        directory_path = "./data/json/search_home"
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)
            print(f"The folder {directory_path} was created.")

        formatted_address = JsonFile.format_str(address)
        json_file_name = f'{directory_path}/{term}_{formatted_address}'
        JsonFile.createJsonFile(_new_products_list, json_file_name)

def getStoreAddressAndName(bearer_token, store_id):
    url = f'https://services.rappi.com.br/api/web-gateway/web/stores-router/id/{store_id}/'

    request_heathers = {
        'authorization' : bearer_token,
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36' 
    }

    try:
        response = requests.get(url, headers=request_heathers)
        response.raise_for_status()
        if response.status_code == 200:
            json_data = response.json()
            store_address = json_data['address']
            store_name = json_data['name']
            return store_address, store_name

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
            stores_list = []
            for store in stores:
                store_dict = {}
                search_term = query
                store_id = store['store_id']
                store_address, store_name = getStoreAddressAndName(bearer_token, store_id)
                products_list = StringUtils.getStoreProdcuts(store, store_id, store_address, store_name, search_term)
                store_dict[store_name] = products_list
                stores_list.append(store_dict)
            
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

def getStoreProducts(_querys, _bearer_token, _search_dict):
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
                    print(term)
                    _search_dict[(query,keyword)] = stores_list
                    return _search_dict, term
                else:
                    print(f'QUERY:{term}:{unit}')
                    print(f'Type diferent unit for {term}')
                    exit()
            else:
                print(f'Insert a keyword for: {query}')
                exit()       
    else:
        print('Input querys')
        exit()

def getFirstQuery(_querys):
    querys_dict = {}
    first_query = list(_querys.items())[0]
    querys_dict[first_query[0]] = first_query[1]
    return querys_dict

"""INPUTS"""

original_queries_dic = {}
if InputSettings.INPUT_SITE:
    clientDetails = InputSettings.SITE[int(sys.argv[1])]   
else: 
    clientDetails = InputSettings.CLIENTS[int(sys.argv[1])]

address = clientDetails["__ADDRESS__"]
client = clientDetails["__NAME__"]
querys = clientDetails["__QUERY__"]
query = getFirstQuery(querys)
AQA.addAditionalQueries(query, original_queries_dic)

"""PROGRAM"""
current_datetime = datetime.now()
formatted_time = current_datetime.strftime("%Y-%m-%d | %H:%M:%S")
print(f'START: {formatted_time}')

print(f'SELECTED CLIENT: {client}')

if len(address) != 0:
    results = geoAddress(address)
    print('Adress OK')
else:
    print('Input an address')
    exit()

current_datetime = datetime.now()
formatted_time = current_datetime.strftime("%Y-%m-%d | %H:%M:%S")
print(f'ADDRESS: {formatted_time}')

# Get the bearer_token
try:
    # bearer_token = Playwright.get_headers_authorization()
    bearer_token = asyncio.run(Playwright.get_bearer_token())
    if bearer_token:
        print('Using generated Bearer_token')
    else:
        print('assync method didnt work')
        exit()
        # token = False
        # while token == False:
        #     bearer_token = Playwright.get_headers_authorization()
        #     if bearer_token:
        #         token = True
        #         print('Using generated Bearer_token with while')            
        
except Exception as err:
    print(f'ERRO: {err}')
    exit()

current_datetime = datetime.now()
formatted_time = current_datetime.strftime("%Y-%m-%d | %H:%M:%S")
print(f'TOKEN: {formatted_time}')

search_dict = {}
search_dict, term = getStoreProducts(query, bearer_token, search_dict)

products_list = []
for stores in search_dict.values():
    for store in stores:
        for store_items in store.values():
            for items in store_items:
                products_list.append(items)

#add datetime 
current_datetime = datetime.now()
formatted_datetime = current_datetime.strftime("%Y-%m-%d | %H:%M:%S")

datetime_products_list = []
for product in products_list:
    items = list(product.items())
    items.insert(0, ('k collected-at', formatted_datetime))
    product = dict(items)
    datetime_products_list.append(product)

current_datetime = datetime.now()
formatted_time = current_datetime.strftime("%Y-%m-%d | %H:%M:%S")
print(f'SCRAPPER: {formatted_time}')

print(f'TOTAL PRODUCTS SCRAPED: {len(datetime_products_list)}')

product_names, store_addresses, product_quantities, product_units, product_prices, product_datetime, product_scores, store_names, product_images = ProductFormatter.getProductsInfo(datetime_products_list)
products_formatted_names = ProductFormatter.setProductsFormattedNames(product_names,product_quantities,product_units)
products_formatted_images = ProductFormatter.setProductsFormattedImages(product_images)
stores_formatted_names = ProductFormatter.setStoresFormattedNames(store_names)
search_home_results = ProductFormatter.sortProductsFromHomePage(products_formatted_names, product_scores, product_prices, store_addresses, products_formatted_images)

setProductsJson(search_home_results, address, term, None)
for product_dict in search_home_results:
    product_name = product_dict['product_name_formatted']
    search_details_results = ProductFormatter.sortProductsFromDetailsPage(product_name, product_prices,store_addresses,product_datetime,products_formatted_names, stores_formatted_names, products_formatted_images)
    setProductsJson(search_details_results, address, None, product_name)

if len(datetime_products_list) > 0:
    GoogleSheetApi.update_google_sheet(clientDetails, datetime_products_list, None, search_home_results, None)
    if InputSettings.INPUT_SITE:
        XlsxUtils.create_csv_file(datetime_products_list)
    if InputSettings.GENERATE_EXCEL:
        FileGenerator.generateFiles(datetime_products_list, clientDetails)

current_datetime = datetime.now()
formatted_time = current_datetime.strftime("%Y-%m-%d | %H:%M:%S")
print(f'FINAL: {formatted_time}')
