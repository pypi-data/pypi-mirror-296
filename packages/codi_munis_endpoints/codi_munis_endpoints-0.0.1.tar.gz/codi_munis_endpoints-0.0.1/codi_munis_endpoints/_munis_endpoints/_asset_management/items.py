class Items:
    def __init__(self, base_url):
        self.base_url = base_url

    def get_odata_IN_v1_items(self):
        '''This endpoint returns item information.'''
        return {
            'method': 'GET',
            'url': f'{self.base_url}/odata/IN/v1/items'
        }

    def get_odata_IN_v1_items_inventory(self):
        '''This endpoint returns inventory item information.'''
        return {
            'method': 'GET',
            'url': f'{self.base_url}/odata/IN/v1/items/inventory'
        }

    def post_api_IN_v1_items_inventory_manualIssue(self):
        '''This endpoint updates the inventory quantity on hand.'''
        return {
            'method': 'POST',
            'url': f'{self.base_url}/api/IN/v1/items/inventory/manualIssue'
        }

    def post_api_IN_v1_items_inventory_manualReceipt(self):
        '''This endpoint records receiving information and will increase available quantity on hand by the amount specified.'''
        return {
            'method': 'POST',
            'url': f'{self.base_url}/api/IN/v1/items/inventory/manualReceipt'
        }

    def get_odata_IN_v1_items_inventory_pickTickets(self):
        '''This endpoint returns pick ticket information.'''
        return {
            'method': 'GET',
            'url': f'{self.base_url}/odata/IN/v1/items/inventory/pickTickets'
        }

    def post_api_IN_v1_items_inventory_pickTickets(self):
        '''This endpoint creates a pick ticket for an inventory item.'''
        return {
            'method': 'POST',
            'url': f'{self.base_url}/api/IN/v1/items/inventory/pickTickets'
        }

    def put_api_IN_v1_items_inventory_pickTickets(self):
        '''This endpoint updates a pick ticket for an inventory item.'''
        return {
            'method': 'PUT',
            'url': f'{self.base_url}/api/IN/v1/items/inventory/pickTickets'
        }

    def get_odata_IN_v1_items_supplier(self):
        '''This endpoint returns supplier item information. Supplier data represents vendors who provide this item, cost, and any associated contract information.'''
        return {
            'method': 'GET',
            'url': f'{self.base_url}/odata/IN/v1/items/supplier'
        }
