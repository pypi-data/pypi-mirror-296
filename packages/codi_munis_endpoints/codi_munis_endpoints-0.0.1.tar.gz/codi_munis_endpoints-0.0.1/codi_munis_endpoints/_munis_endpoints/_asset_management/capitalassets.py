class Capitalassets:
    def __init__(self, base_url):
        self.base_url = base_url

    def get_odata_CA_v1_capitalAssets(self):
        '''This endpoint returns capital asset information.'''
        return {
            'method': 'GET',
            'url': f'{self.base_url}/odata/CA/v1/capitalAssets'
        }

    def post_api_CA_v1_capitalAssets(self):
        '''This endpoint creates a capital asset'''
        return {
            'method': 'POST',
            'url': f'{self.base_url}/api/CA/v1/capitalAssets'
        }

    def put_api_CA_v1_capitalAssets(self):
        '''This endpoint updates a capital asset'''
        return {
            'method': 'PUT',
            'url': f'{self.base_url}/api/CA/v1/capitalAssets'
        }

    def get_api_CA_v1_capitalAssets_{capitalAssetNumber}(self):
        '''This endpoint gets capital assets'''
        return {
            'method': 'GET',
            'url': f'{self.base_url}/api/CA/v1/capitalAssets/{capitalAssetNumber}'
        }
