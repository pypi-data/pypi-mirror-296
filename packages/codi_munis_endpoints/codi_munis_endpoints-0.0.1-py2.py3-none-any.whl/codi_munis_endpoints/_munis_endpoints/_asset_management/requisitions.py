class Requisitions:
    def __init__(self, base_url):
        self.base_url = base_url

    def get_odata_RQ_v1_requisitions(self):
        '''This endpoint returns requisition information.'''
        return {
            'method': 'GET',
            'url': f'{self.base_url}/odata/RQ/v1/requisitions'
        }

    def post_api_RQ_v1_requisitions(self):
        '''This endpoint creates a requisition'''
        return {
            'method': 'POST',
            'url': f'{self.base_url}/api/RQ/v1/requisitions'
        }

    def get_odata_RQ_v1_requisitions_items(self):
        '''This endpoint returns requisition information.'''
        return {
            'method': 'GET',
            'url': f'{self.base_url}/odata/RQ/v1/requisitions/items'
        }
