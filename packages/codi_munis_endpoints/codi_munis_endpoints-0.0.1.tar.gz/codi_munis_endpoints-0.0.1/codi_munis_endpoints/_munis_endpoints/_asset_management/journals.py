class Journals:
    def __init__(self, base_url):
        self.base_url = base_url

    def post_api_GL_v1_journals(self):
        '''This endpoint creates a new Journal entry'''
        return {
            'method': 'POST',
            'url': f'{self.base_url}/api/GL/v1/journals'
        }
