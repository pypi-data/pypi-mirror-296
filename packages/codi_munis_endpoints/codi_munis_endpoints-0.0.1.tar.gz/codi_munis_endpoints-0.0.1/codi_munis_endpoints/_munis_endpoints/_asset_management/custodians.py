class Custodians:
    def __init__(self, base_url):
        self.base_url = base_url

    def get_odata_CA_v1_custodians(self):
        '''This endpoint returns capital asset custodian information.'''
        return {
            'method': 'GET',
            'url': f'{self.base_url}/odata/CA/v1/custodians'
        }
