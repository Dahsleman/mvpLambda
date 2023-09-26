from playwright.sync_api import sync_playwright
from fuzzy.prod.fuzzy_unitary import Fuzzy
import re

class StringUtils:
    @staticmethod
    def getStoreIdAndBrandName(store):
        store_id = store['store_id']
        store_brand_name = store['brand_name']

        if not store_brand_name:
            store_brand_name = store['store_type'].replace('_', '-')
        else:
            store_brand_name = store_brand_name.replace(" ", "-")

        store_brand_name = re.sub('[^0-9a-zA-Z.-]+', '', store_brand_name)
        store_brand_name = store_brand_name.lower()

        return f"{store_id}-{store_brand_name}"
    
    @staticmethod
    def convertToBRPriceDotSystem(price_str:str):
        return price_str.replace(".", "").replace(",", ".")
    
    @staticmethod
    def getStoreName(store:str)->tuple:
        store_brand_name = store['brand_name']

        if not store_brand_name:
            store_brand_name = store['store_type'].replace('_', '-')
        else:
            store_brand_name = store_brand_name.replace(" ", "-")

        store_brand_name = re.sub('[^0-9a-zA-Z.-]+', '', store_brand_name)
        store_brand_name = store_brand_name.lower()

        return store_brand_name
    
    @staticmethod
    def getStoreProdcuts(store:str, store_id:str, store_address:str, store_name:str, search_term:str)->list:
        products = store['products']
        product_dict_list = []
        for product in products:
            product_dict = {}
            can_add = True

            in_stock = product['in_stock']
            product_name = product['name']
            product_score = Fuzzy.main(search_term, product_name)
        
            if in_stock == False or product_score < 70:
                can_add = False

            product_dict['search'] = search_term
            product_dict['store-id'] = store_id
            product_dict['store-address'] = store_address
            product_dict['store-name'] = store_name

            
            product_dict['product-name'] = product_name
            product_dict['product-score'] = product_score

            product_price = product['price']
            product_dict['product-price'] = product_price

            product_unit = product['unit_type']
            product_dict['product-unit'] = product_unit
            
            product_master_id = product['master_product_id']
            if not product_master_id or product_master_id == None or product_master_id == "":
                product_master_id = 'EMPTY'
            product_dict['product-master-id'] = product_master_id

            product_image = product['image']
            product_dict['product-image'] = product_image

            product_quantity = product['quantity']
            product_dict['product-quantity'] = product_quantity


            if can_add:
                product_dict_list.append(product_dict)

        return product_dict_list 

class BearerToken:
    def scrape_network_requests():
        authorization_header = None 

        with sync_playwright() as p:
            chromium = p.chromium
            browser = chromium.launch()
            context = browser.new_context()
            page = context.new_page()

            def route_handler(route, request):
                nonlocal authorization_header 
                if request.method == 'POST' and request.url == 'https://services.rappi.com.br/api/pns-global-search-api/v1/unified-recent-top-searches':
                    authorization_header = request.headers.get('authorization', None)  
                route.continue_()

            page.route('**', route_handler)
            page.goto('https://www.rappi.com.br', timeout=0)
            page.wait_for_selector('body')
            browser.close()

        return authorization_header


