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
    ]

    # Just remember to user / instead of \
    DICTIONARY_FILE_PATH = 'G:/My Drive/kompru/dictionary.xlsx'
    
    DIRECTORY_PATH = "G:/My Drive/kompru/data"

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

    SEARCH_DETAILS = [
        {
            "__ADDRESS__": address,
            "__TERM__":term,
            "__SPREADSHEET_ID__":spreadsheet_id,
            "__PRODUCT_NAME__":'sabonete pielsana liquido antisseptico com phmb 500ml',
        }
    ]
            
        
        