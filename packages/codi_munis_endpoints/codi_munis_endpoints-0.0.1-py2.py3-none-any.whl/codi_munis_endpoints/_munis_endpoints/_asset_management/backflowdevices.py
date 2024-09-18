class Backflowdevices:
    def __init__(self, base_url):
        self.base_url = base_url

    def get_odata_UB_v1_backflowDevices(self):
        '''This endpoint returns backflow device information.'''
        return {
            'method': 'GET',
            'url': f'{self.base_url}/odata/UB/v1/backflowDevices'
        }

    def get_odata_UB_v2_backflowDevices(self):
        '''This endpoint returns backflow device information.'''
        return {
            'method': 'GET',
            'url': f'{self.base_url}/odata/UB/v2/backflowDevices'
        }

    def post_api_UB_v1_backflowDevices(self):
        '''This endpoint inserts a Backflow Device.'''
        return {
            'method': 'POST',
            'url': f'{self.base_url}/api/UB/v1/backflowDevices'
        }

    def put_api_UB_v1_backflowDevices(self):
        '''This endpoint updates a Backflow Device.'''
        return {
            'method': 'PUT',
            'url': f'{self.base_url}/api/UB/v1/backflowDevices'
        }

    def get_odata_UB_v1_backflowDevices_assetTypeCodes(self):
        '''This endpoint returns backflow device asset type code information.'''
        return {
            'method': 'GET',
            'url': f'{self.base_url}/odata/UB/v1/backflowDevices/assetTypeCodes'
        }

    def get_odata_UB_v1_backflowDevices_conditionCodes(self):
        '''This endpoint returns backflow device condition code information.'''
        return {
            'method': 'GET',
            'url': f'{self.base_url}/odata/UB/v1/backflowDevices/conditionCodes'
        }

    def get_odata_UB_v1_backflowDevices_hazardCodes(self):
        '''This endpoint returns backflow device hazard code information.'''
        return {
            'method': 'GET',
            'url': f'{self.base_url}/odata/UB/v1/backflowDevices/hazardCodes'
        }

    def get_odata_UB_v1_backflowDevices_installationTypeCodes(self):
        '''This endpoint returns backflow device installation type code information.'''
        return {
            'method': 'GET',
            'url': f'{self.base_url}/odata/UB/v1/backflowDevices/installationTypeCodes'
        }

    def get_odata_UB_v1_backflowDevices_makeCodes(self):
        '''This endpoint returns backflow device make code information.'''
        return {
            'method': 'GET',
            'url': f'{self.base_url}/odata/UB/v1/backflowDevices/makeCodes'
        }

    def get_odata_UB_v1_backflowDevices_modelCodes(self):
        '''This endpoint returns backflow device model code information.'''
        return {
            'method': 'GET',
            'url': f'{self.base_url}/odata/UB/v1/backflowDevices/modelCodes'
        }

    def get_odata_UB_v1_backflowDevices_serviceTypeCodes(self):
        '''This endpoint returns backflow device service type code information.'''
        return {
            'method': 'GET',
            'url': f'{self.base_url}/odata/UB/v1/backflowDevices/serviceTypeCodes'
        }

    def get_odata_UB_v1_backflowDevices_userDefinedFieldsData(self):
        '''This endpoint returns backflow device user defined fields code information.'''
        return {
            'method': 'GET',
            'url': f'{self.base_url}/odata/UB/v1/backflowDevices/userDefinedFieldsData'
        }

    def post_api_UB_v1_backflowDevices_userDefinedFieldsData(self):
        '''This endpoint creates or updates BackflowDevices user defined fields data'''
        return {
            'method': 'POST',
            'url': f'{self.base_url}/api/UB/v1/backflowDevices/userDefinedFieldsData'
        }
