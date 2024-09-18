class Purchaseorders:
    def __init__(self, base_url):
        self.base_url = base_url

    def get_api_PO_v1_purchaseOrders(self):
        '''This endpoint returns purchase order information.'''
        return {
            'method': 'GET',
            'url': f'{self.base_url}/api/PO/v1/purchaseOrders'
        }

    def post_api_PO_v1_purchaseOrders(self):
        '''This endpoint creates a new purchase order'''
        return {
            'method': 'POST',
            'url': f'{self.base_url}/api/PO/v1/purchaseOrders'
        }

    def get_api_PO_v1_purchaseOrders_statuses(self):
        '''Gets a list of purchase order statuses'''
        return {
            'method': 'GET',
            'url': f'{self.base_url}/api/PO/v1/purchaseOrders/statuses'
        }

    def get_odata_PO_v1_purchaseOrders_userDefinedFields(self):
        '''Gets user defined fields and codes for purchase orders.'''
        return {
            'method': 'GET',
            'url': f'{self.base_url}/odata/PO/v1/purchaseOrders/userDefinedFields'
        }
