class Generalbilling:
    def __init__(self, base_url):
        self.base_url = base_url

    def post_api_AR_v1_generalBillingInvoices(self):
        '''This endpoint creates general billing invoices.'''
        return {
            'method': 'POST',
            'url': f'{self.base_url}/api/AR/v1/generalBillingInvoices'
        }
