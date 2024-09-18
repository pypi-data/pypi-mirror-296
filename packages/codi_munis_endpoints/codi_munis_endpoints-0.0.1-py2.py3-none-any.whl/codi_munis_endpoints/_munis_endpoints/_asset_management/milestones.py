class Milestones:
    def __init__(self, base_url):
        self.base_url = base_url

    def get_odata_PL_v1_milestones(self):
        '''This endpoint returns milestone information'''
        return {
            'method': 'GET',
            'url': f'{self.base_url}/odata/PL/v1/milestones'
        }

    def put_api_PL_v1_milestones(self):
        '''This endpoint updates a milestone'''
        return {
            'method': 'PUT',
            'url': f'{self.base_url}/api/PL/v1/milestones'
        }

    def get_odata_PL_v1_milestones_milestoneCodes(self):
        '''This endpoint returns milestone code information'''
        return {
            'method': 'GET',
            'url': f'{self.base_url}/odata/PL/v1/milestones/milestoneCodes'
        }

    def post_api_PL_v1_milestones_workOrderNumber(self):
        '''This endpoint creates a new milestone'''
        return {
            'method': 'POST',
            'url': f'{self.base_url}/api/PL/v1/milestones/workOrderNumber'
        }
