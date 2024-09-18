class Utilitybillingmeteraccouts:
    def __init__(self, base_url):
        self.base_url = base_url

    def get_odata_UB_v1_utilityBillingAccounts(self):
        '''This endpoint returns meter account information.'''
        return {
            'method': 'GET',
            'url': f'{self.base_url}/odata/UB/v1/utilityBillingAccounts'
        }
