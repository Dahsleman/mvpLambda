from utils.product_formatter_utils import ProductFormatter, JsonFile
from google_sheet.google_sheet_api import GoogleSheetApi
from input_settings import InputSettings
import json
import sys

def setPageTwoList(_products_formatted_names_by_term):
    new_page_two_list = []
    for list in _products_formatted_names_by_term.values():
        for item in list:
            new_page_two_list.append(item)
        
    return new_page_two_list   

clientDetails = InputSettings.SEARCH_DETAILS[int(sys.argv[1])]
address = clientDetails["__ADDRESS__"]
term = clientDetails["__TERM__"]
product_name = clientDetails["__PRODUCT_NAME__"]

directory_path = "./data"
formatted_address = JsonFile.format_str(address)
json_file_name = f'{directory_path}/{term}_{formatted_address}'

try:
    with open(f'{json_file_name}.json', 'r') as json_file:
        existing_data_list = json.load(json_file)
        json_file.close()
except FileNotFoundError as err:
    print(f'Error: {err}')

product_names, store_addresses, product_quantities, product_units, product_prices, product_datetime, product_scores, store_names, product_images = ProductFormatter.getProductsInfo(datetime_products_list)
products_formatted_names = ProductFormatter.setProductsFormattedNames(product_names,product_quantities,product_units)
products_formatted_images = ProductFormatter.setProductsFormattedImages(product_images)

if product_name not in products_formatted_names:
    print('ERRO: Select an existent Produc_name or Address')
    exit()

search_details_results = ProductFormatter.sortProductsFromDetailsPage(product_name, product_prices,store_addresses,product_datetime,products_formatted_names, store_names, products_formatted_images)
GoogleSheetApi.update_google_sheet(clientDetails, None, None, None, search_details_results)

