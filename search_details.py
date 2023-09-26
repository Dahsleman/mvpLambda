from google_sheet.google_sheet_api import GoogleSheetApi
from utils.mvp_utils import ProductFormatter, JsonFile
from input_settings import InputSettings
import json
import sys

def setPageTwoList(_products_formatted_names_by_term):
    new_page_two_list = []
    for list in _products_formatted_names_by_term.values():
        for item in list:
            new_page_two_list.append(item)
        
    return new_page_two_list   

clientDetails = InputSettings.PAGE_TWO[int(sys.argv[1])]
address = clientDetails["__ADDRESS__"]
term = clientDetails["__TERM__"]
product_name = clientDetails["__PRODUCT_NAME__"]

directory_path = "./data"
formatted_address = JsonFile.format_address(address)
json_file_name = f'{directory_path}/{term}_{formatted_address}'

try:
    with open(f'{json_file_name}.json', 'r') as json_file:
        existing_data_list = json.load(json_file)
        json_file.close()
except FileNotFoundError as err:
    print(f'Error: {err}')

product_names, store_addresses, product_quantities, product_units, product_prices, product_datetime, product_scores, store_names = ProductFormatter.getProductsInfo(existing_data_list)
products_formatted_names = ProductFormatter.setProductsFormattedNames(product_names,product_quantities,product_units)

if product_name not in products_formatted_names:
    print('ERRO: Select an existent Produc_name or Address')
    exit()

page_two_list = ProductFormatter.getTermPricesAndStores(product_name, product_prices,store_addresses,product_datetime,products_formatted_names, store_names)
GoogleSheetApi.update_google_sheet(clientDetails, None, None, None, page_two_list)

