class Purchasingdepartments:
    def __init__(self, base_url):
        self.base_url = base_url

    def get_odata_IN_v1_purchasingDepartments(self):
        '''This endpoint returns purchasing department information.'''
        return {
            'method': 'GET',
            'url': f'{self.base_url}/odata/IN/v1/purchasingDepartments'
        }
