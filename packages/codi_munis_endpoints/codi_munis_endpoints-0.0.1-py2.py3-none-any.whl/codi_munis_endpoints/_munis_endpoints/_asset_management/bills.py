class Bills:
    def __init__(self, base_url):
        self.base_url = base_url

    def get_odata_AR_v1_bills(self):
        '''This endpoint returns bill information'''
        return {
            'method': 'GET',
            'url': f'{self.base_url}/odata/AR/v1/bills'
        }

    def get_api_AR_v1_bills_balances(self):
        '''Gets the balances on a bill as of the specified interest effective date.'''
        return {
            'method': 'GET',
            'url': f'{self.base_url}/api/AR/v1/bills/balances'
        }

    def get_odata_AR_v1_bills_details(self):
        '''This endpoint returns bill information'''
        return {
            'method': 'GET',
            'url': f'{self.base_url}/odata/AR/v1/bills/details'
        }

    def get_odata_AR_v2_bills_details(self):
        '''This endpoint returns bill information'''
        return {
            'method': 'GET',
            'url': f'{self.base_url}/odata/AR/v2/bills/details'
        }
