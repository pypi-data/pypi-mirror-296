class Workorders:
    def __init__(self, base_url):
        self.base_url = base_url

    def get_odata_UB_v1_workOrders_approvedByCodes(self):
        '''This endpoint returns work order approved by code information.'''
        return {
            'method': 'GET',
            'url': f'{self.base_url}/odata/UB/v1/workOrders/approvedByCodes'
        }

    def get_odata_UB_v1_workOrders_authorizers(self):
        '''This endpoint returns work order priority code information.'''
        return {
            'method': 'GET',
            'url': f'{self.base_url}/odata/UB/v1/workOrders/authorizers'
        }

    def get_odata_UB_v1_workOrders_crews(self):
        '''This endpoint returns work order priority code information.'''
        return {
            'method': 'GET',
            'url': f'{self.base_url}/odata/UB/v1/workOrders/crews'
        }

    def get_odata_UB_v1_workOrders_customAssignees(self):
        '''This endpoint returns work order priority code information.'''
        return {
            'method': 'GET',
            'url': f'{self.base_url}/odata/UB/v1/workOrders/customAssignees'
        }

    def get_odata_UB_v1_workOrders_departments(self):
        '''This endpoint returns work orders'''
        return {
            'method': 'GET',
            'url': f'{self.base_url}/odata/UB/v1/workOrders/departments'
        }

    def get_odata_UB_v1_workOrders_priorityCodes(self):
        '''This endpoint returns work order priority code information.'''
        return {
            'method': 'GET',
            'url': f'{self.base_url}/odata/UB/v1/workOrders/priorityCodes'
        }

    def get_odata_UB_v1_workOrders_reasonCodes(self):
        '''This endpoint returns work order reason code information.'''
        return {
            'method': 'GET',
            'url': f'{self.base_url}/odata/UB/v1/workOrders/reasonCodes'
        }

    def get_odata_UB_v1_workOrders_serviceDetails(self):
        '''This endpoint returns work orders'''
        return {
            'method': 'GET',
            'url': f'{self.base_url}/odata/UB/v1/workOrders/serviceDetails'
        }

    def get_api_UB_v1_workOrders_statuses(self):
        '''This endpoint gets available status information.'''
        return {
            'method': 'GET',
            'url': f'{self.base_url}/api/UB/v1/workOrders/statuses'
        }

    def get_odata_UB_v1_workOrders_typeCodes(self):
        '''This endpoint returns work order type code information.'''
        return {
            'method': 'GET',
            'url': f'{self.base_url}/odata/UB/v1/workOrders/typeCodes'
        }
