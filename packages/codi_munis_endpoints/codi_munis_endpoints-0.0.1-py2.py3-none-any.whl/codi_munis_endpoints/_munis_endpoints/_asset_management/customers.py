class Customers:
    def __init__(self, base_url):
        self.base_url = base_url

    def get_odata_AR_v1_customers(self):
        '''This endpoint returns customer information'''
        return {
            'method': 'GET',
            'url': f'{self.base_url}/odata/AR/v1/customers'
        }

    def get_odata_AR_v1_customers_addresses(self):
        '''This endpoint returns customer information'''
        return {
            'method': 'GET',
            'url': f'{self.base_url}/odata/AR/v1/customers/addresses'
        }

    def get_odata_AR_v1_customers_emailAddresses(self):
        '''This endpoint returns customer information'''
        return {
            'method': 'GET',
            'url': f'{self.base_url}/odata/AR/v1/customers/emailAddresses'
        }

    def get_odata_AR_v1_customers_phoneNumbers(self):
        '''This endpoint returns customer information'''
        return {
            'method': 'GET',
            'url': f'{self.base_url}/odata/AR/v1/customers/phoneNumbers'
        }

    def get_api_UB_v1_customers_utilityBillingData(self):
        '''This endpoint gets customers utility billing data.'''
        return {
            'method': 'GET',
            'url': f'{self.base_url}/api/UB/v1/customers/utilityBillingData'
        }
