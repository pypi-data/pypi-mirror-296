from ....hubspot_api.helpers.hubspot import HubspotConnectorApi, Endpoints
from ....hubspot_api.properties import read_all

from ....hubspot_api.helpers.get_dataframe import next_page, get_dataframe
from typing import Optional
import pandas as pd

import requests


class Teams():
    def __init__(self, client:HubspotConnectorApi):
        self.client = client
        
    def call(self, after:int = 0, limit:int = 100) -> requests.Response:
        querystring = {"limit":limit,"after":after}
        response = requests.request("GET", self.client.settings_endpoint(Endpoints.USERS_TEAMS), headers=self.client.headers, params=querystring)
        print(self.client.settings_endpoint(Endpoints.USERS_TEAMS))
        return response
    
    def all_pages_df(self) -> Optional[pd.DataFrame]:
        after = 0
        dfs = []

        while after != None:
            rq = self.call(after)
            if rq.status_code == 200:
                df = get_dataframe(rq)
                dfs.append(df)
                after = next_page(rq.json())
            else:
                return None

        return pd.concat(dfs).reset_index(drop=True)