class Userdefinedfields:
    def __init__(self, base_url):
        self.base_url = base_url

    def get_odata_UB_v1_userDefinedFields_backflowDevices(self):
        '''This endpoint returns user defined field codes information.'''
        return {
            'method': 'GET',
            'url': f'{self.base_url}/odata/UB/v1/userDefinedFields/backflowDevices'
        }

    def get_odata_UB_v1_userDefinedFields_flatInventory(self):
        '''This endpoint returns custom field codes information.'''
        return {
            'method': 'GET',
            'url': f'{self.base_url}/odata/UB/v1/userDefinedFields/flatInventory'
        }

    def get_odata_UB_v1_userDefinedFields_meters(self):
        '''This endpoint returns custom field codes information.'''
        return {
            'method': 'GET',
            'url': f'{self.base_url}/odata/UB/v1/userDefinedFields/meters'
        }
