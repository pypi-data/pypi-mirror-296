class Invoices:
    def __init__(self, base_url):
        self.base_url = base_url

    def get_odata_AP_v1_invoices(self):
        '''This endpoint returns invoice information.'''
        return {
            'method': 'GET',
            'url': f'{self.base_url}/odata/AP/v1/invoices'
        }

    def post_api_AP_v1_invoices(self):
        '''This endpoint creates an invoice which represents a record to be paid to a vendor.'''
        return {
            'method': 'POST',
            'url': f'{self.base_url}/api/AP/v1/invoices'
        }

    def get_odata_AP_v1_invoices_details(self):
        '''This endpoint returns invoice information.'''
        return {
            'method': 'GET',
            'url': f'{self.base_url}/odata/AP/v1/invoices/details'
        }

    def get_odata_AP_v1_invoices_pCardTransactions(self):
        '''This endpoint returns invoice information.'''
        return {
            'method': 'GET',
            'url': f'{self.base_url}/odata/AP/v1/invoices/pCardTransactions'
        }

    def post_api_AP_v1_invoices_postBatch(self):
        '''This endpoint posts approved invoices within a batch.'''
        return {
            'method': 'POST',
            'url': f'{self.base_url}/api/AP/v1/invoices/postBatch'
        }

    def get_api_PO_v1_invoices_paymentMethods(self):
        '''Gets a list of invoice payment methods.'''
        return {
            'method': 'GET',
            'url': f'{self.base_url}/api/PO/v1/invoices/paymentMethods'
        }
