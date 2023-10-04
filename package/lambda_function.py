from utils.product_formatter_utils import ProductFormatter
from utils.rappi_utils import StringUtils
from input_settings import InputSettings
from geopy.geocoders import GoogleV3
from datetime import datetime
import requests
import json

def lambda_handler(event, context):
    return {
        'statusCode': 200,
        'headers': [
            "Access-Control-Allow-Origin" "*",
            "Access-Control-Allow-Methods" "GET, POST, OPTIONS"
        ],
        'body': event    
    }

def set_search_home_data(_products_list:list, _term:str)->dict:
    _products_dict = {}
    _products_dict['search_term'] = _term
    _products_dict['search_home_results_count'] = len(_products_list)
    _products_dict['search_home_results'] = _products_list
    return _products_dict

def get_bearer_token():
    url_passport = "https://services.rappi.com.br/api/rocket/v2/guest/passport"
    request_heathers = {
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'deviceid':'34a6a2f7-2291-43c7-8bc3-98b2dd5b7e67'
    }

    try:
        response = requests.get(url_passport, headers=request_heathers)
        if response.status_code == 200:
            json_data = response.json()
            token = json_data['token']
            url_guest = "https://services.rappi.com.br/api/rocket/v2/guest"
            request_heathers = {
                'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
                'deviceid':'34a6a2f7-2291-43c7-8bc3-98b2dd5b7e67',
                'X-Guest-API-Key': token
            }
            try:
                response = requests.post(url_guest, headers=request_heathers)
                if response.status_code == 200:
                    json_data = response.json()
                    access_token = json_data['access_token']
                    bearer_token = f'Bearer {access_token}'
                    return bearer_token

            except requests.exceptions.HTTPError as err:
                print(f'ERRO URL GUEST: {err}')
                exit()

    except requests.exceptions.HTTPError as err:
        print(f'ERRO URL PASSPORT: {err}')
        exit()

def get_store_address_and_name(bearer_token, store_id):
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

def stores_list(lat, lng, query, bearer_token):
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
                store_address, store_name = get_store_address_and_name(bearer_token, store_id)
                products_list = StringUtils.get_store_products(store, store_id, store_address, store_name, search_term)
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

def convert_address_into_coordinates(address:str)->tuple:
    api_key = "AIzaSyB2NcBN7WcYDQiBF8MZ1iKiMVl4SSDlcbI"
    geolocator = GoogleV3(api_key=api_key)
    location = geolocator.geocode(address)
    lat = location.latitude
    lng = location.longitude
    return lat, lng

"""INPUTS"""
address = InputSettings.ADDRESS
term = InputSettings.TERM

"""PROGRAM"""
current_datetime = datetime.now()
formatted_time = current_datetime.strftime("%Y-%m-%d | %H:%M:%S")
print(f'START: {formatted_time}')

if len(address) != 0:
    lat, lng = convert_address_into_coordinates(address)
    print('Adress OK')
else:
    print('Input an address')
    exit()

current_datetime = datetime.now()
formatted_time = current_datetime.strftime("%Y-%m-%d | %H:%M:%S")
print(f'ADDRESS: {formatted_time}')

# Get the bearer_token
bearer_token = get_bearer_token()

current_datetime = datetime.now()
formatted_time = current_datetime.strftime("%Y-%m-%d | %H:%M:%S")
print(f'TOKEN: {formatted_time}')

products_list = []
stores = stores_list(lat, lng, term, bearer_token )
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

(product_names, store_addresses, 
 product_quantities, product_units, 
 product_prices, product_datetime, 
 product_scores, store_names, product_images) = ProductFormatter.get_products_info(datetime_products_list)

products_formatted_names = ProductFormatter.set_products_formatted_names(product_names,product_quantities,product_units)

products_formatted_images = ProductFormatter.set_products_formatted_images(product_images)

stores_formatted_names = ProductFormatter.set_stores_formatted_names(store_names)

search_home_results = ProductFormatter.sort_products_from_home_page(products_formatted_names, product_scores, 
                                                                    product_prices, store_addresses, 
                                                                    products_formatted_images)

addresses_formatted_names = ProductFormatter.set_addresses_formatted_names(store_addresses)

for product_dict in search_home_results:
    product_name_formatted = product_dict['product_name_formatted']
    search_details_results = ProductFormatter.sort_products_from_details_page(product_name_formatted, product_prices, 
                                                                              addresses_formatted_names, product_datetime, 
                                                                              products_formatted_names, stores_formatted_names, 
                                                                              products_formatted_images)

    product_dict['product_image_url'] = search_details_results[0]['product_image']
    for details_dict in search_details_results:
        details_dict.pop('product_image')

    product_dict['search_details_results'] = search_details_results

data_dict = set_search_home_data(search_home_results, term)

# file_path = "data/lambda.json"
# with open(file_path, 'w') as json_file:
#     json.dump(data_dict, json_file, indent=4)

json_data = json.dumps(data_dict, indent=4)

if InputSettings.SAVE_S3:
    InputSettings.S3.put_object(Bucket=InputSettings.SAVE_BUCKET_NAME, Key=InputSettings.SAVE_FILE_KEY, Body=json_data)
    lambda_handler(json_data, None)

current_datetime = datetime.now()
formatted_time = current_datetime.strftime("%Y-%m-%d | %H:%M:%S")
print(f'FINAL: {formatted_time}')

