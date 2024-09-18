class Budgetcodes:
    def __init__(self, base_url):
        self.base_url = base_url

    def get_api_GL_v1_budgetCodes(self):
        '''Gets a list of budget codes'''
        return {
            'method': 'GET',
            'url': f'{self.base_url}/api/GL/v1/budgetCodes'
        }
