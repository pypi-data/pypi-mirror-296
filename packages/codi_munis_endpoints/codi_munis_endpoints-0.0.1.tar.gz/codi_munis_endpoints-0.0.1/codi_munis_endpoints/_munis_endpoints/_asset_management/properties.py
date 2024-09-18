class Properties:
    def __init__(self, base_url):
        self.base_url = base_url

    def get_odata_CEN_v1_properties(self):
        '''This endpoint returns property information.'''
        return {
            'method': 'GET',
            'url': f'{self.base_url}/odata/CEN/v1/properties'
        }
