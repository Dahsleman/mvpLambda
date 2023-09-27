import json

class InputSettings:
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
            
        
        