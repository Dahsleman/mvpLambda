from collections import defaultdict 
import unicodedata
import json
import os

class ProductFormatter:

    def sortProductsWithSameCountByLowestPrice(products_formatted_names:list, product_scores:list, product_count:list, product_prices:list, product_stores:list, product_images:list)->tuple:
        products_list = []
        scores_list = []
        count_list = []
        prices_list = []
        stores_list = []
        images_list = []
        
        for formatted_name, score, count, price, store, image in zip(products_formatted_names, product_scores, product_count, product_prices, product_stores, product_images):
            append = True
            position_to_insert = 0
            if len(prices_list) == 0:
                products_list.append(formatted_name)
                scores_list.append(score)
                count_list.append(count)
                prices_list.append(price)
                stores_list.append(store)
                images_list.append(image)
                append = False
            else:
                for index ,item_price in enumerate(prices_list):
                    if item_price > price:
                        append = False
                        position_to_insert = index
                        products_list.insert(position_to_insert, formatted_name)
                        scores_list.insert(position_to_insert, score)
                        count_list.insert(position_to_insert, count)
                        prices_list.insert(position_to_insert, price)
                        stores_list.insert(position_to_insert, store)    
                        images_list.insert(position_to_insert, image)                
                        break
            if append:
                products_list.append(formatted_name)
                prices_list.append(price)
                count_list.append(count)
                scores_list.append(score)
                stores_list.append(store)
                images_list.append(image)

        return products_list, scores_list, count_list, prices_list, stores_list, images_list
    
    def sortProductsByPrice(products_formatted_names:list, product_scores:list, product_count:list, product_prices:list, product_stores:list, product_images:list)->tuple:
        new_product_names = []
        new_product_scores = []
        new_product_count = []
        new_product_prices = []
        new_product_stores = []
        new_product_images = []
        temp_product_names = []
        temp_product_scores = []
        temp_product_count = []
        temp_product_prices = []
        temp_product_stores = []
        temp_product_images = []
        
        while len(product_count) != 0:
            highest_count = product_count[0]
            for name,score,count, price, store, image in zip(products_formatted_names, product_scores, product_count, product_prices, product_stores, product_images):
                if count == highest_count:    
                    if name not in new_product_names:
                        temp_product_names.append(name)
                        temp_product_scores.append(score)
                        temp_product_count.append(count)
                        temp_product_prices.append(price)
                        temp_product_stores.append(store)
                        temp_product_images.append(image)
            
            if len(temp_product_names) !=0:
                temp_product_names, temp_product_scores, temp_product_count, temp_product_prices, temp_product_stores, temp_product_images = ProductFormatter.sortProductsWithSameCountByLowestPrice(temp_product_names,temp_product_scores, temp_product_count,temp_product_prices, temp_product_stores, temp_product_images)
                for name, score, count, price, store, images in zip (temp_product_names, temp_product_scores, temp_product_count, temp_product_prices, temp_product_stores, temp_product_images):
                    new_product_names.append(name)
                    new_product_scores.append(score)
                    new_product_count.append(count)
                    new_product_prices.append(price)
                    new_product_stores.append(store)
                    new_product_images.append(image)

            temp_product_names.clear()
            temp_product_count.clear()
            temp_product_prices.clear()
            temp_product_scores.clear()
            temp_product_stores.clear()
            temp_product_images.clear()
            for index, count in enumerate(product_count):
                if count == highest_count:
                    products_formatted_names.pop(index)
                    product_scores.pop(index)
                    product_count.pop(index)
                    product_prices.pop(index)
                    product_stores.pop(index)
                    product_images.pop(index)
                    
        return new_product_names, new_product_scores, new_product_count, new_product_prices, new_product_stores, new_product_images

    def sortProductsWithSameScoreByHighestCount(products_formatted_names:list, product_scores:list, product_count:list, product_prices:list, product_stores:list, product_images:list)->tuple:
        products_list = []
        scores_list = []
        count_list = []
        prices_list = []
        stores_list = []
        images_list = []
        
        for formatted_name, score, count, price, store, image in zip(products_formatted_names, product_scores, product_count, product_prices, product_stores, product_images):
            append = True
            position_to_insert = 0
            if len(count_list) == 0:
                products_list.append(formatted_name)
                scores_list.append(score)
                count_list.append(count)
                prices_list.append(price)
                stores_list.append(store)
                images_list.append(image)
                append = False
            else:
                for index ,item_count in enumerate(count_list):
                    if item_count < count:
                        append = False
                        position_to_insert = index
                        products_list.insert(position_to_insert, formatted_name)
                        scores_list.insert(position_to_insert, score)
                        count_list.insert(position_to_insert, count)
                        prices_list.insert(position_to_insert, price)
                        stores_list.insert(position_to_insert, store)
                        images_list.insert(position_to_insert, image)
                        break
            if append:
                products_list.append(formatted_name)
                scores_list.append(score)
                count_list.append(count)
                prices_list.append(price)
                stores_list.append(store)
                images_list.append(image)

        return products_list, scores_list, count_list, prices_list, stores_list, images_list 
    
    def sortProductsbyCount(products_formatted_names:list, product_scores:list, product_count:list, product_prices:list, product_stores:list, product_images:list)->list:
        new_product_names = []
        new_product_count = []
        new_product_prices = []
        new_product_scores = []
        new_product_stores = []
        new_product_images = []
        temp_product_names = []
        temp_product_count = []
        temp_product_prices = []
        temp_product_scores = []
        temp_product_stores = []
        temp_product_images = []

        while len(product_scores) != 0:
            highest_score = product_scores[0]
            for name ,score,count, price, store, image in zip(products_formatted_names, product_scores, product_count, product_prices, product_stores, product_images):
                if score == highest_score:    
                    if name not in new_product_names:
                        temp_product_names.append(name)
                        temp_product_count.append(count)
                        temp_product_prices.append(price)
                        temp_product_scores.append(score)
                        temp_product_stores.append(store)
                        temp_product_images.append(image)
            
            if len(temp_product_names) !=0:
                temp_product_names, temp_product_scores, temp_product_count, temp_product_prices, temp_product_stores, temp_product_images = ProductFormatter.sortProductsWithSameScoreByHighestCount(temp_product_names,temp_product_scores, temp_product_count,temp_product_prices, temp_product_stores, temp_product_images)         
                temp_product_names, temp_product_scores, temp_product_count, temp_product_prices, temp_product_stores, temp_product_images = ProductFormatter.sortProductsByPrice(temp_product_names,temp_product_scores, temp_product_count,temp_product_prices, temp_product_stores, temp_product_images)
                
                for name, score, count, price, store, image  in zip (temp_product_names, temp_product_scores, temp_product_count, temp_product_prices, temp_product_stores, temp_product_images):
                    new_product_names.append(name)
                    new_product_count.append(count)
                    new_product_prices.append(price)
                    new_product_scores.append(score)
                    new_product_stores.append(store)
                    new_product_images.append(image)

            temp_product_names.clear()
            temp_product_count.clear()
            temp_product_prices.clear()
            temp_product_scores.clear()
            temp_product_stores.clear()
            temp_product_images.clear()
            for index, score in enumerate(product_scores):
                if score == highest_score:
                    products_formatted_names.pop(index)
                    product_scores.pop(index)
                    product_count.pop(index)
                    product_prices.pop(index)
                    product_stores.pop(index)
                    product_images.pop(index)
                    
        return new_product_names, new_product_scores, new_product_count, new_product_prices, new_product_stores, new_product_images

    def getProductNamesHigherScoreAndCountAndStartPrice(products_formatted_names:list, product_scores:list, product_prices:list, product_stores:list, product_images:list)->list:
        formatted_names_dict = defaultdict(list)
        
        for formatted_name , score, price, store, image in zip(products_formatted_names, product_scores, product_prices, product_stores, product_images):
            if len(formatted_names_dict[formatted_name])==0:
                product_dict = {}
                store_list = []
                store_list.append(store)
                image_list = []
                image_list.append(image)
                product_dict['name'] = formatted_name
                product_dict['score'] = score
                product_dict['count'] = 1
                product_dict['start-price'] = price
                product_dict['stores'] = 1
                product_dict['images'] = image
                formatted_names_dict[formatted_name].append(product_dict)
                formatted_names_dict[formatted_name].append(store_list)
                formatted_names_dict[formatted_name].append(image_list)  

            else:
                product_dict = formatted_names_dict[formatted_name][0]
                product_dict['count'] +=1
                actual_score = product_dict['score']
                if score > actual_score:
                    product_dict['score'] = score
                actual_price = product_dict['start-price']
                if price < actual_price:
                    product_dict['start-price'] = price
                append = False

                store_list = formatted_names_dict[formatted_name][1]
                for store_address in store_list:
                    if store != store_address:
                        append = True
                if append:
                    product_dict['stores'] += 1
                    store_list.append(store)

                # image_list = formatted_names_dict[formatted_name][2]
                # for image_url in image_list:
                #     if image != image_url:
                #         print('ERROR:One formatted name with two diferent images')
                #         print(image_url)
                #         print(image)
                #         exit()
                
        name_list = []
        score_list = []
        count_list = []
        start_price_list = []
        stores_list = []
        images_list = []

        for product_dict_list in list(formatted_names_dict.values()):
            product_dict = product_dict_list[0]
            for key,value in product_dict.items():
                if key == 'name':
                    name_list.append(value)
                elif key == 'score':
                    score_list.append(value)
                elif key == 'count':
                    count_list.append(value)
                elif key == 'start-price':
                    start_price_list.append(value)
                elif key == 'stores':
                    stores_list.append(value)
                elif key == 'images':
                    images_list.append(value)

        return name_list, score_list, count_list, start_price_list, stores_list, images_list

    def sortProductsByHighestScore(products_formatted_names:list, product_scores:list, product_prices:list, product_stores:list, product_images:list)->tuple:
        products_list = []
        scores_list = []
        prices_list = []
        stores_list = []
        images_list = []
        
        for formatted_name, score, price, store, image  in zip(products_formatted_names, product_scores, product_prices, product_stores, product_images):    
            append = True
            position_to_insert = 0
            if len(scores_list) == 0:
                products_list.append(formatted_name)
                scores_list.append(score)
                prices_list.append(price)
                stores_list.append(store)
                images_list.append(image)
                append = False
            else:
                for index ,item_score in enumerate(scores_list):
                    if item_score < score:
                        append = False
                        position_to_insert = index
                        products_list.insert(position_to_insert, formatted_name)
                        scores_list.insert(position_to_insert, score)
                        prices_list.insert(position_to_insert, price)
                        stores_list.insert(position_to_insert, store)
                        images_list.insert(position_to_insert, image)
                        break
            if append:
                products_list.append(formatted_name)
                prices_list.append(price)
                scores_list.append(score)
                stores_list.append(store)
                images_list.append(image)

        return products_list, scores_list, prices_list , stores_list, images_list

    def sort_products_from_home_page(products_formatted_names:list, product_scores:list, product_prices:list, product_stores:list, product_images:list)->list:
        product_names_sorted = []
        
        name_list, score_list, start_price_list, stores_list, images_list  = ProductFormatter.sortProductsByHighestScore(products_formatted_names, product_scores, product_prices, product_stores, product_images)
        name_list, score_list, count_list, start_price_list, stores_list, images_list = ProductFormatter.getProductNamesHigherScoreAndCountAndStartPrice(name_list, score_list, start_price_list, stores_list, images_list) 
        name_list, score_list, count_list, start_price_list, stores_list, images_list = ProductFormatter.sortProductsbyCount(name_list, score_list, count_list, start_price_list, stores_list, images_list)

        for name, score, count, price, store, image in zip(name_list, score_list, count_list, start_price_list, stores_list, images_list):
            product_dict = {}
            product_dict['product_name_formatted'] = name
            # product_dict['count'] = count
            product_dict['lowest_price'] = price
            product_dict['stores_with_item'] = store
            product_dict['product_image_url'] = image
            product_dict['fuzzy_score'] = score

            product_names_sorted.append(product_dict)
        
        return product_names_sorted

    def sort_products_by_lowest_price(product_names:list, product_prices:list, product_store_names:list, product_store_addresses:list, product_images:list)->tuple:
        products_list = []
        prices_list = []
        store_names_list = []
        store_addresses_list = []
        images_list = []

        for name, price, store_name, store_addresses, image in zip(product_names, product_prices, product_store_names, product_store_addresses, product_images):
            append = True
            position_to_insert = 0
            if len(prices_list) == 0:
                products_list.append(name)
                prices_list.append(price)
                store_names_list.append(store_name)
                store_addresses_list.append(store_addresses)
                images_list.append(image)
                append = False
            else:
                for index ,item_price in enumerate(prices_list):
                    if item_price > price:
                        append = False
                        position_to_insert = index
                        products_list.insert(position_to_insert, name)
                        prices_list.insert(position_to_insert, price)
                        store_names_list.insert(position_to_insert, store_name)  
                        store_addresses_list.insert(position_to_insert, store_addresses) 
                        images_list.insert(position_to_insert,image)              
                        break
            if append:
                products_list.append(name)
                prices_list.append(price)
                store_names_list.append(store_name)
                store_addresses_list.append(store_addresses)
                images_list.append(image)

        return products_list, prices_list, store_names_list, store_addresses_list, images_list
        
    def sort_products_from_details_page(product_name:str, product_prices:list, store_address:list, datetime_search:list, products_formatted_names:list, store_names:list, product_images:list )->list:
        product_names_by_term = []
        new_product_names = []
        new_product_prices = []
        new_product_store_names = []
        new_product_store_addresses = []
        new_product_images = []

        for formatted_name, price, store_name,store_address, image in zip(products_formatted_names, product_prices, store_names,store_address, product_images):
            if  product_name == formatted_name:
                new_product_names.append(formatted_name)
                new_product_prices.append(price)
                new_product_store_names.append(store_name)
                new_product_store_addresses.append(store_address)
                new_product_images.append(image)

        new_product_names, new_product_prices, new_product_store_names,new_product_store_addresses, new_product_images = ProductFormatter.sort_products_by_lowest_price(new_product_names, new_product_prices, new_product_store_names,new_product_store_addresses, new_product_images)
        for formatted_name, price, store_name,store_address, datetime, image in zip(new_product_names, new_product_prices, new_product_store_names,new_product_store_addresses,datetime_search, new_product_images):
            if  product_name == formatted_name:    
                product_dict = {}
                # product_dict['product-name'] = formatted_name
                product_dict['product_price'] = price
                product_dict['store_name'] = store_name
                product_dict['store_address'] = store_address
                product_dict['product_image'] = image
                product_dict['collected_at'] = datetime
                product_names_by_term.append(product_dict)

        return product_names_by_term

    def set_addresses_formatted_names(store_address:list)->list:
        address_formatted_names = []
        for address in store_address:
            address = unicodedata.normalize('NFKD', address).encode('ASCII', 'ignore').decode('ASCII')
            # formatted_name = bytes(name, 'utf-8').decode('unicode-escape')
            formatted_address = address
            address_formatted_names.append(formatted_address)
        return address_formatted_names
    
    def set_stores_formatted_names(store_names:list)->list:
        stores_formatted_names = []
        for name in store_names:
            name = unicodedata.normalize('NFKD', name).encode('ASCII', 'ignore').decode('ASCII')
            # formatted_name = bytes(name, 'utf-8').decode('unicode-escape')
            formatted_name = name
            stores_formatted_names.append(formatted_name)
        return stores_formatted_names
    
    def set_products_formatted_images(product_images:list)->list:
        products_formatted_images = []
        for image in product_images:
            formatted_image = f'https://images.rappi.com.br/products/{image}'
            
            products_formatted_images.append(formatted_image)
        return products_formatted_images
    
    def set_products_formatted_names(product_names:list, quantities:list,units:list)->list:
        products_formatted_names = []
        for name, qty, unit in zip(product_names, quantities, units):
            name = unicodedata.normalize('NFKD', name).encode('ASCII', 'ignore').decode('ASCII')
            formatted_name = name.lower().strip()

            if qty is not None and float(qty) != 0.0:
                formatted_name = f"{formatted_name} {qty}{unit}"
            
            products_formatted_names.append(formatted_name)
        return products_formatted_names

    def get_products_info(products_list:list)->tuple:
        product_names = []
        store_addresses = []
        product_quantities = []
        product_units = []
        product_prices = []
        product_datetime = []
        product_scores = []
        store_names = []
        product_images = []
        for products_dict in products_list:
            for header,value in products_dict.items():
                if header == 'product-name':
                    product_names.append(value)
                elif header == 'store-address':
                    store_addresses.append(value)
                elif header == 'product-quantity':
                    product_quantities.append(value)
                elif header == 'product-unit':
                    product_units.append(value)
                elif header == 'product-price':
                    product_prices.append(value)
                elif header == 'k collected-at':
                    product_datetime.append(value)
                elif header == 'product-score':
                    product_scores.append(value)
                elif header == 'store-name':
                    store_names.append(value)
                elif header == 'product-image':
                    product_images.append(value)

        return product_names, store_addresses, product_quantities, product_units, product_prices, product_datetime, product_scores, store_names, product_images
    
class JsonFile:
    def create_json_file(products_list:list, file_path:str):
        _products_list = []
        for product in products_list:
            _products_list.append(product)
        with open(f'{file_path}.json', 'w') as fp:
            json.dump(_products_list, fp, indent=1)
            fp.close()
    
    def set_json(_products_list:list, address:str, term=None, product_name=None)->json:
        if term == None:
            _new_products_list = []
            _products_dict = {}
            _products_dict['status'] = 200
            _products_dict['product_formatted_name'] = product_name
            _products_dict['search_details_results_count'] = len(_products_list)
            _products_dict['search_details_results'] = _products_list
            _new_products_list.append(_products_dict)

            directory_path = "./data/search_details"
            if not os.path.exists(directory_path):
                os.makedirs(directory_path)
                print(f"The folder {directory_path} was created.")

            formatted_name = JsonFile.format_str(product_name)
            formatted_address = JsonFile.format_str(address)
            json_file_name = f'{directory_path}/{formatted_name}_{formatted_address}'
            JsonFile.create_json_file(_new_products_list, json_file_name)

        elif product_name == None:
            _new_products_list = []
            _products_dict = {}
            _products_dict['status'] = 200
            _products_dict['search_home_results_count'] = len(_products_list)
            _products_dict['search_home_results'] = _products_list
            _new_products_list.append(_products_dict)
            
            directory_path = "./data/search_details"
            if not os.path.exists(directory_path):
                os.makedirs(directory_path)
                print(f"The folder {directory_path} was created.")

            formatted_address = JsonFile.format_str(address)
            json_file_name = f'{directory_path}/{term}_{formatted_address}'
            JsonFile.create_json_file(_new_products_list, json_file_name)

    def format_str(input_str:str)->str:
        # Split the string into words
        words = input_str.split()

        # Capitalize the first letter of each word and join them
        capitalized_words = [word.capitalize() for word in words]

        # Join the capitalized words into a single string
        formatted_input = ''.join(capitalized_words)

        # Remove spaces, commas, dots, and hyphens
        formatted_input = formatted_input.replace(' ', '').replace(',', '').replace('.', '').replace('-', '').replace('/', '')

        return formatted_input