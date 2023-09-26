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
]

#### Adicionar bibliotecas para rodar google sheet api
  pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib

##### mvp.py:
    Para rodar e colocar no terminal python mvp.py 0 (tem que ter o "zero" no final)
    

