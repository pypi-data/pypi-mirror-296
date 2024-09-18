class Servicemeters:
    def __init__(self, base_url):
        self.base_url = base_url

    def get_api_UB_v1_serviceMeters_statuses(self):
        '''This endpoint gets service meter statuses.'''
        return {
            'method': 'GET',
            'url': f'{self.base_url}/api/UB/v1/serviceMeters/statuses'
        }
