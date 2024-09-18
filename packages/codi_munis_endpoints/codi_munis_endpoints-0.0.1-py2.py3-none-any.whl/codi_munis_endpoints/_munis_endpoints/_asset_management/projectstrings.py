class Projectstrings:
    def __init__(self, base_url):
        self.base_url = base_url

    def get_odata_PL_v1_projectStrings(self):
        '''This endpoint returns project string information.'''
        return {
            'method': 'GET',
            'url': f'{self.base_url}/odata/PL/v1/projectStrings'
        }

    def get_odata_PL_v1_projectStrings_balances(self):
        '''This endpoint returns project string balance information.'''
        return {
            'method': 'GET',
            'url': f'{self.base_url}/odata/PL/v1/projectStrings/balances'
        }
