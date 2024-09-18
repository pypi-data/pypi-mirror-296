class Purchaseorderreceipts:
    def __init__(self, base_url):
        self.base_url = base_url

    def get_odata_PO_v1_purchaseOrders_receipts(self):
        '''This endpoint retrieves existing purchase order receipts.'''
        return {
            'method': 'GET',
            'url': f'{self.base_url}/odata/PO/v1/purchaseOrders/receipts'
        }

    def post_api_PO_v1_purchaseOrders_receipts(self):
        '''This endpoint creates a new purchase order receipt.'''
        return {
            'method': 'POST',
            'url': f'{self.base_url}/api/PO/v1/purchaseOrders/receipts'
        }

    def put_api_PO_v1_purchaseOrders_receipts(self):
        '''This endpoint updates existing purchase order receipt'''
        return {
            'method': 'PUT',
            'url': f'{self.base_url}/api/PO/v1/purchaseOrders/receipts'
        }
