import pandas as pd
import json

class InputSettings:
    CLIENTS = [
        {
            "__NAME__": "MVP",
            "__ADDRESS__": 'R. Prof. Baroni, 190 - 101 - Gutierrez, Belo Horizonte - MG, 30441-180',
            "__QUERY__": {
                ("leite","L"):(),
            },
            "__SPREADSHEET_ID__": '1lzEl5fIgC4PfC2PuA7zJBUfs8TrSY6wGHwG3ktUQRzs'
        },
    ]

    # Just remember to user / instead of \
    DICTIONARY_FILE_PATH = 'G:/My Drive/kompru/dictionary.xlsx'
    
    DIRECTORY_PATH = "G:/My Drive/kompru/data"

    directory_path = "./data/s3"
    json_file_name = f'{directory_path}/input'

    try:
        with open(f'{json_file_name}.json', 'r') as json_file:
            json_data = json.load(json_file)
            json_file.close()
    except FileNotFoundError as err:
        print(f'Error: {err}')

    term = json_data['search_term']
    address = json_data['address']

    LAMBDA = [
        {
            "__ADDRESS__": address,
            "__QUERY__": {
                (term,"L"):(),
            },
            "__TERM__": term,
        }
    ]
            
        
        