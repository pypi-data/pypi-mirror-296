class Userdefinedfieldscodes:
    def __init__(self, base_url):
        self.base_url = base_url

    def get_odata_UB_v1_userDefinedFieldsCodes_backflowDevices(self):
        '''This endpoint returns custom field codes information.'''
        return {
            'method': 'GET',
            'url': f'{self.base_url}/odata/UB/v1/userDefinedFieldsCodes/backflowDevices'
        }

    def get_odata_UB_v1_userDefinedFieldsCodes_flatInventory(self):
        '''This endpoint returns custom field codes information.'''
        return {
            'method': 'GET',
            'url': f'{self.base_url}/odata/UB/v1/userDefinedFieldsCodes/flatInventory'
        }

    def get_odata_UB_v1_userDefinedFieldsCodes_meters(self):
        '''This endpoint returns custom field codes information.'''
        return {
            'method': 'GET',
            'url': f'{self.base_url}/odata/UB/v1/userDefinedFieldsCodes/meters'
        }
