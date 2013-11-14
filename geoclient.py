from configuration import *

class GeoClient:
    def __init__(self, format = 'json'):
        self.builtins = {
            'app_id': GEOCLIENT_APP_ID,
            'app_key': GEOCLIENT_APP_KEY
        }
        self.base_url = 'https://api.cityofnewyork.us/geoclient/v1/'
        self.format = format
        self.boroughs = {
            1:'manhattan',
            2:'bronx',
            3:'brooklyn',
            4:'queens',
            5:'staten island'
        }
        
    def __query(self, params):
        # Merge with app_id and app_key
        params = dict(params.items() + self.builtins.items())
        
        # Form a query
        
    def standardize(self, address):
        '''
        This function will return the standardize version of address 
        '''
        
        # Extract house number, street name and borough
        #1. House number: The first numerical value (including hyphen)
        #2. Street name: The rest
        #3. Borough: Hard to infer. Manhattan + Brooklyn is easy but Queens is harder