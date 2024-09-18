class Munisusers:
    def __init__(self, base_url):
        self.base_url = base_url

    def get_odata_MUN_v1_munisUsers(self):
        '''This endpoint returns munis user's information.'''
        return {
            'method': 'GET',
            'url': f'{self.base_url}/odata/MUN/v1/munisUsers'
        }
