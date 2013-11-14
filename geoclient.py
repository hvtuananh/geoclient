from configuration import *
import re
import json
import urllib, urllib2
import traceback

addr_p = re.compile(r'([\d\-]+)([^,]+)(.+)', re.I)
borough_p = re.compile(r'brooklyn|manhattan|')
zip_p = re.compile(r'\d{5}')

class GeoClient:
    def __init__(self, format = 'json'):
        self.builtins = {
            'app_id': GEOCLIENT_APP_ID,
            'app_key': GEOCLIENT_APP_KEY
        }
        self.base_url = 'https://api.cityofnewyork.us/geoclient/v1/'
        self.format = format
        self.boroughs = {
            '1':'manhattan',
            '2':'bronx',
            '3':'brooklyn',
            '4':'queens',
            '5':'staten island',
            '100':'manhattan',
            '104':'bronx',
            '112':'brooklyn',
            '113':'queens',
            '114':'queens',
            '111':'queens',
            '116':'queens',
            '110':'queens',
            '103':'staten island'
        }
        self.max_retry = 10
        
    def __query(self, params):
        # Merge with app_id and app_key
        params = dict(params.items() + self.builtins.items())
        
        # Form a query
        url = self.base_url + 'address.' + self.format + '?' + urllib.urlencode(params)
        
        # Make query
        retry = 0
        data = None
        while retry < self.max_retry:
            try:
                # Only support JSON at this moment
                data = json.load(urllib2.urlopen(url))
            except:
                traceback.print_exc()
                retry += 1
            break
        if data is None or data['address'] is None or data['address']['geosupportReturnCode'][0:1] is not '0' or int(data['address']['geosupportReturnCode']) > 1:
            return None
        return data['address']
                
    def __infer_borough(self, string):
        '''
        There are 2 ways of inferring borough from address string:
        1. Look at zip code (easier): http://www.health.ny.gov/statistics/cancer/registry/appendix/neighborhoods.htm
        2. Find borough information using regular expression (not always correct)
        
        Let's follow the first direction!
        '''
        candidates = string.split(',')
        zip_candidate = candidates[len(candidates)-1]
        matches = zip_p.search(zip_candidate)
        if not matches:
            return None
            
        zip = matches.group(0)
        if zip[0:1] is not '1':
            return None
        return self.boroughs[zip[0:3]]
        
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
            'street': street,
            'borough':borough
        }
        
        results = self.__query(params)
        return results

if __name__ == '__main__':        
    geo = GeoClient()
    print geo.standardize('1085 E 12 ST, , BROOKLYN, NY, 11330')