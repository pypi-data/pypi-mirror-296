class Projects:
    def __init__(self, base_url):
        self.base_url = base_url

    def get_odata_GL_v1_projects(self):
        '''This endpoint returns project information'''
        return {
            'method': 'GET',
            'url': f'{self.base_url}/odata/GL/v1/projects'
        }
