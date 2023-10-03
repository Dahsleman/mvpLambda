import boto3
import json

class InputSettings:
    
    INPUT_S3 = True
    S3 = boto3.client('s3')
    INPUT_BUCKET_NAME = 'input.json'
    INPUT_FILE_KEY = 'input.json'

    SAVE_S3 = True
    SAVE_BUCKET_NAME = 'search-home.json'
    SAVE_FILE_KEY = 'search_home'
    
    if INPUT_S3 == False:
        directory_path = "."
        json_file_name = f'{directory_path}/input'
        try:
            with open(f'{json_file_name}.json', 'r') as json_file:
                json_data = json.load(json_file)
                json_file.close()
        except FileNotFoundError as err:
            print(f'Error: {err}')
    elif INPUT_S3 == True:
        response = S3.get_object(Bucket=INPUT_BUCKET_NAME, Key=INPUT_FILE_KEY)
        json_data = json.loads(response['Body'].read().decode('utf-8'))

    TERM = json_data['search_term']
    ADDRESS = json_data['address']
            
        
        