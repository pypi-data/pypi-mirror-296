class Chargecodes:
    def __init__(self, base_url):
        self.base_url = base_url

    def get_odata_AR_v1_chargeCodes(self):
        '''This endpoint returns charge code information'''
        return {
            'method': 'GET',
            'url': f'{self.base_url}/odata/AR/v1/chargeCodes'
        }
