class Paytypes:
    def __init__(self, base_url):
        self.base_url = base_url

    def get_odata_PR_v2_payTypes(self):
        '''This endpoint returns pay types'''
        return {
            'method': 'GET',
            'url': f'{self.base_url}/odata/PR/v2/payTypes'
        }
