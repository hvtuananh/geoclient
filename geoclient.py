from configuration import *
import re

addr_p = re.compile(r'([\d\-]+)([^,]+)(.+)', re.I)

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
        matches = addr_p.search(address)
        
        # If address is mal-formed
        if not matches:
            return None
            
        # The funny thing
        house_number = str(matches.group(1).replace('-', ''))
        street = str(matches.group(2)).strip()
        borough = self.__infer_borough(matches.group(3))
        
        params = {
            'houseNumber': house_number,
            'street': street 
            
        }
        return params     
        
geo = GeoClient()
print geo.standardize('xxx 74-07 6666 62nd St, Brooklyn, NY')