import pandas as pd

class InputSettings:
    CLIENTS = [
        {
            "__NAME__": "MVP",
            "__ADDRESS__": 'R. Prof. Baroni, 190 - 101 - Gutierrez, Belo Horizonte - MG, 30441-180',
            "__QUERY__": {
                ("saco de lixo","kg"):(),
            },
            "__SPREADSHEET_ID__": '1lzEl5fIgC4PfC2PuA7zJBUfs8TrSY6wGHwG3ktUQRzs'
        },
        {
            "__NAME__":"lucas_bhering_4",
            "__ADDRESS__": 'R. Castelo de Lisboa, 280 - Castelo, Belo Horizonte - MG, 31330-452',
            "__QUERY__": {
                ("freestyle libre","und"):(),
                ("insulina tresiba","L"):(),
                ("insulina fiasp","L"):(),
                ("bravecto 10 kg","und"):(),
                ("insulina degludeca","L"):(),
                },
            "__SPREADSHEET_ID__":'1lVd-7z-B2lX5N_Ff-fW1MAefEacjAkU5OGfN222btQU'
        },
    ]

    # Just remember to user / instead of \
    DICTIONARY_FILE_PATH = 'G:/My Drive/kompru/dictionary.xlsx'

    # THE UNIT IS SECONDS 60 * 2 = 120 seconds = 2 minutes
    # 1 HOUR = 60 * 60
    # 2 HOURS = 60 * 60 * 2
    AUTO_SCRIPT_SCHEDULER_TIME = 1

    # Save products-out-stock in .xlsx?
    # True  -> Save only products-out-stock = False in .xlsx file
    # False -> Save products-out-stock = True or False in .xlsx file
    ONLY_AVAILABLE_PRODUCTS = False

    # Save match-search-term? in .xlsx?
    # True  -> Save only match-search-term? = True in .xlsx file
    # False -> Save match-search-term? = True or False in .xlsx file
    ONLY_MATCH_SEARCH_TERM_PRODUCTS = False

    # Save product-input-price = incompativel in .xlsx?
    # True  -> Save only product-input-price != incompativel in .xlsx file
    # False -> Save all product-input-price in .xlsx file
    ONLY_COMPATIBLE_PRICES_PRODUCTS = False
    
    DIRECTORY_PATH = "G:/My Drive/kompru/data"
 
    # Excel Header columns
    EXCEL_HEADER = ['k collected-at',         'k term',                   'k unit-input', 
                    'store-id',               'store-type',               'product-id',
                    'master-product-id',      'product-price',            'product-real-price',
                    'product-unit',           'k product-size',           'k unit-input-size',
                    'k product-input-unit',   'k product-input-price',    'k match-unit-input?',
                    'product-name',           'k term-in-product-name?',  'product-out-stock',
                    'step-quantity-in-grams']

    INPUT_SITE = False
    GENERATE_EXCEL = False
    WORKBOOK_PATH = './Workbook.xlsx'

    df_name = pd.read_excel(WORKBOOK_PATH, sheet_name='name')
    df_address = pd.read_excel(WORKBOOK_PATH, sheet_name='address')
    df_query = pd.read_excel(WORKBOOK_PATH, sheet_name='query')
    df_spreadsheet_id = pd.read_excel(WORKBOOK_PATH, sheet_name='spreadsheet_id')

    for i in df_name.index:
        name = df_name.iloc[i]['Name']
        address = df_address.iloc[i]['Address']
        term = df_query.iloc[i]['Query']  
        query_dict = {(term, "kg"): ()}  
        spreadsheet_id = df_spreadsheet_id.iloc[i]['Spreadsheet_ID']

    SITE = [
        {
            "__NAME__": name,
            "__ADDRESS__": address,
            "__QUERY__": query_dict, 
            "__SPREADSHEET_ID__": spreadsheet_id
        }    
    ] 

    PAGE_TWO = [
        {
            "__ADDRESS__": address,
            "__TERM__":term,
            "__SPREADSHEET_ID__":spreadsheet_id,
            "__PRODUCT_NAME__":'sabonete pielsana liquido antisseptico com phmb 500ml',
        }
    ]
            
        
        