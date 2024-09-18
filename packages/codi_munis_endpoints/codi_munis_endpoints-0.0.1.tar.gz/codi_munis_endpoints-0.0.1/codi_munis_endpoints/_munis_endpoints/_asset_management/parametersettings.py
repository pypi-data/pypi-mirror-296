class Parametersettings:
    def __init__(self, base_url):
        self.base_url = base_url

    def get_odata_GL_v1_parameterSettings(self):
        '''This endpoint returns GL parameter settings'''
        return {
            'method': 'GET',
            'url': f'{self.base_url}/odata/GL/v1/parameterSettings'
        }
