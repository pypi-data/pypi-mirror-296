import requests

def get_ticket_page(url
                    ,email:str
                    ,token:str):

    # Hacer la solicitud GET a la API de Zendesk
    response = requests.get(url, auth=(f'{email}/token', token))

    # Verificar que la solicitud fue exitosa
    if response.status_code == 200:
        data = response.json()
        # Aquí puedes procesar los datos del reporte como necesites
        return data
    else:
        print(f'Error: {response.status_code}')