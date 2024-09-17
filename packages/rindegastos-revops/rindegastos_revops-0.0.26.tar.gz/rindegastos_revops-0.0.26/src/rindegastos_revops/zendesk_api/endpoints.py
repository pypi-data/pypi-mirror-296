from enum import Enum

class Endpoints(Enum):
    TICKETS = 'tickets.json'
    ORGANIZATIONS = 'organizations.json'
    USERS = 'users.json'

class API(Enum):
    V2 = 'https://rindegastoshelp.zendesk.com/api/v2/'


def construct_url(api:API
                  ,endpoint:Endpoints
                  ,parameters:str='?page[size]=100&sort=id')->str:
    
    return f'{api.value}{endpoint.value}{parameters}'