class Conditions:
    def __init__(self, base_url):
        self.base_url = base_url

    def get_odata_CA_v1_conditions(self):
        '''This endpoint returns capital asset condition information.'''
        return {
            'method': 'GET',
            'url': f'{self.base_url}/odata/CA/v1/conditions'
        }
