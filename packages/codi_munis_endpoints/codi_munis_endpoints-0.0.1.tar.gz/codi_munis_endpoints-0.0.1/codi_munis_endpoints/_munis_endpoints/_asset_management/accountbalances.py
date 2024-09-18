class Accountbalances:
    def __init__(self, base_url):
        self.base_url = base_url

    def get_odata_GL_v1_accountBalances(self):
        '''This endpoint returns account balance information'''
        return {
            'method': 'GET',
            'url': f'{self.base_url}/odata/GL/v1/accountBalances'
        }
