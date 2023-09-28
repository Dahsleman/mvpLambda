import search_home

def lambda_handler(event, context):
    search_home()
    return {
        'statusCode': 200,
        'body': 'deu certo'
    }