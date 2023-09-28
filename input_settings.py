import json

class InputSettings:
    directory_path = "."
    json_file_name = f'{directory_path}/input'

    try:
        with open(f'{json_file_name}.json', 'r') as json_file:
            json_data = json.load(json_file)
            json_file.close()
    except FileNotFoundError as err:
        print(f'Error: {err}')

    TERM = json_data['search_term']
    ADDRESS = json_data['address']
            
        
        