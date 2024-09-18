class Backflowdevicetypes:
    def __init__(self, base_url):
        self.base_url = base_url

    def get_odata_UB_v1_backflowDeviceTypes(self):
        '''This endpoint returns backflow device information.'''
        return {
            'method': 'GET',
            'url': f'{self.base_url}/odata/UB/v1/backflowDeviceTypes'
        }
