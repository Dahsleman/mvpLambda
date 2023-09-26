from collections import Counter, defaultdict 
import unicodedata
import json

class ProductFormatter:

    def sortProductsWithSameCountByLowestPrice(products_formatted_names:list, product_scores:list, product_count:list, product_prices:list, product_stores:list)->tuple:
        products_list = []
        scores_list = []
        count_list = []
        prices_list = []
        stores_list = []
        
        for formatted_name, score, count, price, store in zip(products_formatted_names, product_scores, product_count, product_prices, product_stores):
            append = True
            position_to_insert = 0
            if len(prices_list) == 0:
                products_list.append(formatted_name)
                scores_list.append(score)
                count_list.append(count)
                prices_list.append(price)
                stores_list.append(store)
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
                        break
            if append:
                products_list.append(formatted_name)
                prices_list.append(price)
                count_list.append(count)
                scores_list.append(score)
                stores_list.append(store)

        return products_list, scores_list, count_list, prices_list, stores_list
    
    def sortProductsByPrice(products_formatted_names:list, product_scores:list, product_count:list, product_prices:list, product_stores:list):
        new_product_names = []
        new_product_scores = []
        new_product_count = []
        new_product_prices = []
        new_product_stores = []
        temp_product_names = []
        temp_product_scores = []
        temp_product_count = []
        temp_product_prices = []
        temp_product_stores = []
        
        while len(product_count) != 0:
            highest_count = product_count[0]
            for name,score,count, price, store in zip(products_formatted_names, product_scores, product_count, product_prices, product_stores):
                if count == highest_count:    
                    if name not in new_product_names:
                        temp_product_names.append(name)
                        temp_product_scores.append(score)
                        temp_product_count.append(count)
                        temp_product_prices.append(price)
                        temp_product_stores.append(store)
            
            if len(temp_product_names) !=0:
                temp_product_names, temp_product_scores, temp_product_count, temp_product_prices, temp_product_stores = ProductFormatter.sortProductsWithSameCountByLowestPrice(temp_product_names,temp_product_scores, temp_product_count,temp_product_prices, temp_product_stores)
                for name, score, count, price, store in zip (temp_product_names, temp_product_scores, temp_product_count, temp_product_prices, temp_product_stores):
                    new_product_names.append(name)
                    new_product_scores.append(score)
                    new_product_count.append(count)
                    new_product_prices.append(price)
                    new_product_stores.append(store)

            temp_product_names.clear()
            temp_product_count.clear()
            temp_product_prices.clear()
            temp_product_scores.clear()
            temp_product_stores.clear()
            for index, count in enumerate(product_count):
                if count == highest_count:
                    products_formatted_names.pop(index)
                    product_scores.pop(index)
                    product_count.pop(index)
                    product_prices.pop(index)
                    product_stores.pop(index)
                    
        return new_product_names, new_product_scores, new_product_count, new_product_prices, new_product_stores

    def sortProductsWithSameScoreByHighestCount(products_formatted_names:list, product_scores:list, product_count:list, product_prices:list, product_stores:list)->tuple:
        products_list = []
        scores_list = []
        count_list = []
        prices_list = []
        stores_list = []
        
        for formatted_name, score, count, price, store in zip(products_formatted_names, product_scores, product_count, product_prices, product_stores):
            append = True
            position_to_insert = 0
            if len(count_list) == 0:
                products_list.append(formatted_name)
                scores_list.append(score)
                count_list.append(count)
                prices_list.append(price)
                stores_list.append(store)
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
                        break
            if append:
                products_list.append(formatted_name)
                scores_list.append(score)
                count_list.append(count)
                prices_list.append(price)
                stores_list.append(store)

        return products_list, scores_list, count_list, prices_list, stores_list 
    
    def sortProductsbyCount(products_formatted_names:list, product_scores:list, product_count:list, product_prices:list, product_stores:list)->list:
        new_product_names = []
        new_product_count = []
        new_product_prices = []
        new_product_scores = []
        new_product_stores = []
        temp_product_names = []
        temp_product_count = []
        temp_product_prices = []
        temp_product_scores = []
        temp_product_stores = []

        while len(product_scores) != 0:
            highest_score = product_scores[0]
            for name ,score,count, price, store in zip(products_formatted_names, product_scores, product_count, product_prices, product_stores):
                if score == highest_score:    
                    if name not in new_product_names:
                        temp_product_names.append(name)
                        temp_product_count.append(count)
                        temp_product_prices.append(price)
                        temp_product_scores.append(score)
                        temp_product_stores.append(store)
            
            if len(temp_product_names) !=0:
                temp_product_names, temp_product_scores, temp_product_count, temp_product_prices, temp_product_stores = ProductFormatter.sortProductsWithSameScoreByHighestCount(temp_product_names,temp_product_scores, temp_product_count,temp_product_prices, temp_product_stores)         
                temp_product_names, temp_product_scores, temp_product_count, temp_product_prices, temp_product_stores = ProductFormatter.sortProductsByPrice(temp_product_names,temp_product_scores, temp_product_count,temp_product_prices, temp_product_stores)
                
                for name, score, count, price, store  in zip (temp_product_names, temp_product_scores, temp_product_count, temp_product_prices, temp_product_stores):
                    new_product_names.append(name)
                    new_product_count.append(count)
                    new_product_prices.append(price)
                    new_product_scores.append(score)
                    new_product_stores.append(store)

            temp_product_names.clear()
            temp_product_count.clear()
            temp_product_prices.clear()
            temp_product_scores.clear()
            temp_product_stores.clear()
            for index, score in enumerate(product_scores):
                if score == highest_score:
                    products_formatted_names.pop(index)
                    product_scores.pop(index)
                    product_count.pop(index)
                    product_prices.pop(index)
                    product_stores.pop(index)
                    
        return new_product_names, new_product_scores, new_product_count, new_product_prices, new_product_stores 

    def getProductNamesHigherScoreAndCountAndStartPrice(products_formatted_names:list, product_scores:list, product_prices:list, product_stores:list)->list:
        formatted_names_dict = defaultdict(list)
        
        for formatted_name , score, price, store in zip(products_formatted_names, product_scores, product_prices, product_stores):
            if len(formatted_names_dict[formatted_name])==0:
                product_dict = {}
                store_list = []
                store_list.append(store)
                product_dict['name'] = formatted_name
                product_dict['score'] = score
                product_dict['count'] = 1
                product_dict['start-price'] = price
                product_dict['stores'] = 1
                formatted_names_dict[formatted_name].append(product_dict)
                formatted_names_dict[formatted_name].append(store_list)   
            else:
                product_dict = formatted_names_dict[formatted_name][0]
                store_list = formatted_names_dict[formatted_name][1]
                
                product_dict['count'] +=1
                actual_score = product_dict['score']
                if score > actual_score:
                    product_dict['score'] = score
                actual_price = product_dict['start-price']
                if price < actual_price:
                    product_dict['start-price'] = price
                append = False
                for store_address in store_list:
                    if store != store_address:
                        append = True
                if append:
                    product_dict['stores'] += 1
                    store_list.append(store)
                
        name_list = []
        score_list = []
        count_list = []
        start_price_list = []
        stores_list = []

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

        return name_list, score_list, count_list, start_price_list, stores_list

    def sortProductsByHighestScore(products_formatted_names:list, product_scores:list, product_prices:list, product_stores:list)->tuple:
        products_list = []
        scores_list = []
        prices_list = []
        stores_list = []
        
        for formatted_name, score, price, store  in zip(products_formatted_names, product_scores, product_prices, product_stores):
            
            append = True
            position_to_insert = 0
            if len(scores_list) == 0:
                products_list.append(formatted_name)
                scores_list.append(score)
                prices_list.append(price)
                stores_list.append(store)
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
                        break
            if append:
                products_list.append(formatted_name)
                prices_list.append(price)
                scores_list.append(score)
                stores_list.append(store)

        return products_list, scores_list, prices_list , stores_list

    def sortProductsFromPageOne(products_formatted_names:list, product_scores:list, product_prices:list, product_stores:list):
        product_names_sorted = []
        
        name_list, score_list, start_price_list, stores_list  = ProductFormatter.sortProductsByHighestScore(products_formatted_names, product_scores, product_prices, product_stores)
        name_list, score_list, count_list, start_price_list, stores_list = ProductFormatter.getProductNamesHigherScoreAndCountAndStartPrice(name_list, score_list, start_price_list, stores_list) 
        name_list, score_list, count_list, start_price_list, stores_list = ProductFormatter.sortProductsbyCount(name_list, score_list, count_list, start_price_list, stores_list)

        for name, score, count, price, store in zip(name_list, score_list, count_list, start_price_list, stores_list):
            product_dict = {}
            product_dict['product-name'] = name
            product_dict['score'] = score
            product_dict['count'] = count
            product_dict['start-price'] = price
            product_dict['stores'] = store

            product_names_sorted.append(product_dict)
        
        return product_names_sorted

    def sortProductsByLowestPrice(product_names:list, product_prices:list, product_store_names:list, product_store_addresses:list):
        products_list = []
        prices_list = []
        store_names_list = []
        store_addresses_list = []

        for name, price, store_name, store_addresses in zip(product_names, product_prices, product_store_names, product_store_addresses):
            append = True
            position_to_insert = 0
            if len(prices_list) == 0:
                products_list.append(name)
                prices_list.append(price)
                store_names_list.append(store_name)
                store_addresses_list.append(store_addresses)
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
                        break
            if append:
                products_list.append(name)
                prices_list.append(price)
                store_names_list.append(store_name)
                store_addresses_list.append(store_addresses)

        return products_list, prices_list, store_names_list, store_addresses_list
        
    def getTermPricesAndStores(product_name:str, product_prices:list, store_address:list, datetime_search:list, products_formatted_names:list, store_names:list )->dict:
        formatted_names_by_term = defaultdict(list)
        product_names_by_term = []
        new_product_names = []
        new_product_prices = []
        new_product_store_names = []
        new_product_store_addresses = []

        for formatted_name, price, store_name,store_address in zip(products_formatted_names, product_prices, store_names,store_address):
            if  product_name == formatted_name:
                new_product_names.append(formatted_name)
                new_product_prices.append(price)
                new_product_store_names.append(store_name)
                new_product_store_addresses.append(store_address)

        new_product_names, new_product_prices, new_product_store_names,new_product_store_addresses = ProductFormatter.sortProductsByLowestPrice(new_product_names, new_product_prices, new_product_store_names,new_product_store_addresses)
        for formatted_name, price, store_name,store_address, datetime in zip(new_product_names, new_product_prices, new_product_store_names,new_product_store_addresses,datetime_search):
            if  product_name == formatted_name:    
                product_dict = {}
                product_dict['product-name'] = formatted_name
                product_dict['price'] = price
                product_dict['store'] = store_name
                product_dict['address'] = store_address
                product_dict['collected-in'] = datetime
                product_names_by_term.append(product_dict)

        return product_names_by_term

    def setProductsFormattedNames(product_names:list, quantities:list,units:list)->list:
        products_formatted_names = []
        for name, qty, unit in zip(product_names, quantities, units):
            name = unicodedata.normalize('NFKD', name).encode('ASCII', 'ignore').decode('ASCII')
            formatted_name = name.lower().strip()

            if qty is not None and float(qty) != 0.0:
                formatted_name = f"{formatted_name} {qty}{unit}"
            
            products_formatted_names.append(formatted_name)
        return products_formatted_names

    def getProductsInfo(products_list:list)->tuple:
        product_names = []
        store_addresses = []
        product_quantities = []
        product_units = []
        product_prices = []
        product_datetime = []
        product_scores = []
        store_names = []
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

        return product_names, store_addresses, product_quantities, product_units, product_prices, product_datetime, product_scores, store_names
    
class JsonFile:
    def createJsonFile(products_list:list, file_path:str):
        _products_list = []
        for product in products_list:
            _products_list.append(product)
        with open(f'{file_path}.json', 'w') as fp:
            json.dump(_products_list, fp, indent=1)
            fp.close()

    def format_address(input_address):
        # Split the string into words
        words = input_address.split()

        # Capitalize the first letter of each word and join them
        capitalized_words = [word.capitalize() for word in words]

        # Join the capitalized words into a single string
        formatted_address = ''.join(capitalized_words)

        # Remove spaces, commas, dots, and hyphens
        formatted_address = formatted_address.replace(' ', '').replace(',', '').replace('.', '').replace('-', '')

        return formatted_address