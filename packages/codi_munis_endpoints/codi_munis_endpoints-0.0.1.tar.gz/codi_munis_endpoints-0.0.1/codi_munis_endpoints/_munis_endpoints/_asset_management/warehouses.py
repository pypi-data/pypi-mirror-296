class Warehouses:
    def __init__(self, base_url):
        self.base_url = base_url

    def get_odata_AP_v1_warehouses(self):
        '''This endpoint returns warehouse code information. Warehouses represent locations from which inventory is stocked.'''
        return {
            'method': 'GET',
            'url': f'{self.base_url}/odata/AP/v1/warehouses'
        }
