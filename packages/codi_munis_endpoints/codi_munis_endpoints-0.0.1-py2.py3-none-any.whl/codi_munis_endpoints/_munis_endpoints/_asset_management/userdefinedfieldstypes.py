class Userdefinedfieldstypes:
    def __init__(self, base_url):
        self.base_url = base_url

    def get_odata_MUN_v1_userDefinedFieldsTypes(self):
        '''This endpoint returns user defined data field types.'''
        return {
            'method': 'GET',
            'url': f'{self.base_url}/odata/MUN/v1/userDefinedFieldsTypes'
        }
