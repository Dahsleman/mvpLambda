# rappi-scrapper

## Input Settings:
Utilize o input_settings.py para adicionar as configuracoes iniciais como as queries, o endereco, o cliente, etc.

### CLIENTS
CLIENTS é uma lista de dicionarios, ou seja, cada dicionario possui 3 chaves:
__NAME__, __ADDRESS__ e __QUERY__, representando o nome, o endereço(Colocar o endereco igual no google maps) e a lista de busca do cliente. Voce pode adicionar quantos clientes quiser, basta seguir o padrao:

Exemplo do cliente1 e cliente2
CLIENTS = [

    {
        "__NAME__": "cliente1",
        "__ADDRESS__": "Endereco",
        "__QUERY__": {
            ("busca 1", "kg"):(''),
            ("busca 2", "kg"):(''),
            ...
        },
        "__SPREADSHEET_ID__": '1XTu2y-SN1gTU5JZvJ5SwYnHGr67e_wIDndoYBAluUYI'
    }

    {
        "__NAME__": "cliente2",
        "__ADDRESS__": "Endereco 2",
        "__QUERY__": {
            ("busca 3", "kg"):(''),
            ("busca 4", "kg"):(''),
            ...
        },
        "__SPREADSHEET_ID__": '1XTu2y-SN1gTU5JZvJ5SwYnHGr67e_wIDndoYBAluUYI'
    }
]

#### Adicionar bibliotecas para rodar google sheet api
  pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib

#### DIRECTORY_PATH
Colocar qual o "path" da pasta em que vao ficar os dados escrapados (.json, .xlsx).
Exemplo:
Se for colocar os dados no google drive dentro da pasta chamada "data" que esta dentro da pasta "kompru":
DIRECTORY_PATH = "G:/My Drive/kompru/data"

##### excel
Utilize excel.py sempre que quiser criar/atualizar o arquivo de excel com .json 

Exemplo de colunas:


    {
        "k collected-at": "2023-08-14 | 20:19:00",
        "k term": "LEITE INTEGRAL",
        "k unit-input": "l",
        "store-id": "900130437",
        "store-type": "carrefour-hiper-super-market",
        "product-id": "2093584338",
        "master-product-id": "1655539",
        "product-price": 5.49,
        "product-real-price": 5.49,
        "product-unit": "(5.49/l)",
        "k product-size": "1 l",
        "k unit-input-size": 1.0,
        "k product-input-unit": "(5.49/l)",
        "k product-input-price": 5.49,
        "k match-unit-input?": "True",
        "product-name": "Itamb\u00e9 Leite Uht Integral",
        "k term-in-product-name?": "True"
    }
