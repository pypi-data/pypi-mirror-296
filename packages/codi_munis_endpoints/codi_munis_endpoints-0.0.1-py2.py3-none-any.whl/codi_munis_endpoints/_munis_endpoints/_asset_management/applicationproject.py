class Applicationproject:
    def __init__(self, base_url):
        self.base_url = base_url

    def get_api_PI_v1_applicationProject(self, applicationReference):
        '''This endpoint gets the application project'''
        return {
            'method': 'GET',
            'url': f'{self.base_url}/api/PI/v1/applicationProject/{applicationReference}'
        }
