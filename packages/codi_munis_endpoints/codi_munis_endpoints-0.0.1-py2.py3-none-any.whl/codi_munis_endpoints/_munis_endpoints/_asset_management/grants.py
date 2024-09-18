class Grants:
    def __init__(self, base_url):
        self.base_url = base_url

    def get_odata_PL_v1_grants(self):
        '''This endpoint returns milestone information'''
        return {
            'method': 'GET',
            'url': f'{self.base_url}/odata/PL/v1/grants'
        }
