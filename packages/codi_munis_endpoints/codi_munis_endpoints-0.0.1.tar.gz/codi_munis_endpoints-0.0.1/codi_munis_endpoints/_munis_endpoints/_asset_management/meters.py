class Meters:
    def __init__(self, base_url):
        self.base_url = base_url

    def get_odata_UB_v1_meters(self):
        '''This endpoint returns meter information.'''
        return {
            'method': 'GET',
            'url': f'{self.base_url}/odata/UB/v1/meters'
        }

    def get_odata_UB_v2_meters(self):
        '''This endpoint returns meter information.'''
        return {
            'method': 'GET',
            'url': f'{self.base_url}/odata/UB/v2/meters'
        }

    def post_api_UB_v1_meters(self):
        '''This endpoint inserts a meter.'''
        return {
            'method': 'POST',
            'url': f'{self.base_url}/api/UB/v1/meters'
        }

    def put_api_UB_v1_meters(self):
        '''This endpoint updates a meter.'''
        return {
            'method': 'PUT',
            'url': f'{self.base_url}/api/UB/v1/meters'
        }

    def get_odata_UB_v1_meters_assetTypes(self):
        '''This endpoint returns meter asset type information.'''
        return {
            'method': 'GET',
            'url': f'{self.base_url}/odata/UB/v1/meters/assetTypes'
        }

    def get_odata_UB_v1_meters_circleCodes(self):
        '''This endpoint returns meter circle code information.'''
        return {
            'method': 'GET',
            'url': f'{self.base_url}/odata/UB/v1/meters/circleCodes'
        }

    def get_odata_UB_v1_meters_conditionCodes(self):
        '''This endpoint returns meter condition code information.'''
        return {
            'method': 'GET',
            'url': f'{self.base_url}/odata/UB/v1/meters/conditionCodes'
        }

    def get_odata_UB_v1_meters_details(self):
        '''This endpoint returns meter detail information.'''
        return {
            'method': 'GET',
            'url': f'{self.base_url}/odata/UB/v1/meters/details'
        }

    def get_odata_UB_v1_meters_details_services(self):
        '''This endpoint returns meter detail information.'''
        return {
            'method': 'GET',
            'url': f'{self.base_url}/odata/UB/v1/meters/details/services'
        }

    def get_odata_UB_v1_meters_deviceCodes(self):
        '''This endpoint returns meter device code information.'''
        return {
            'method': 'GET',
            'url': f'{self.base_url}/odata/UB/v1/meters/deviceCodes'
        }

    def get_odata_UB_v1_meters_flowTypeCodes(self):
        '''This endpoint returns meter flow type code information.'''
        return {
            'method': 'GET',
            'url': f'{self.base_url}/odata/UB/v1/meters/flowTypeCodes'
        }

    def get_odata_UB_v1_meters_modelCodes(self):
        '''This endpoint returns meter model code information.'''
        return {
            'method': 'GET',
            'url': f'{self.base_url}/odata/UB/v1/meters/modelCodes'
        }

    def get_api_UB_v1_meters_readCodes(self):
        '''This endpoint gets available meter read codes information.'''
        return {
            'method': 'GET',
            'url': f'{self.base_url}/api/UB/v1/meters/readCodes'
        }

    def get_api_UB_v1_meters_reasonCodes(self):
        '''This endpoint gets available meter reason codes information.'''
        return {
            'method': 'GET',
            'url': f'{self.base_url}/api/UB/v1/meters/reasonCodes'
        }

    def get_odata_UB_v1_meters_sizeCodes(self):
        '''This endpoint returns meter size code information.'''
        return {
            'method': 'GET',
            'url': f'{self.base_url}/odata/UB/v1/meters/sizeCodes'
        }

    def get_api_UB_v1_meters_statuses(self):
        '''This endpoint gets meter statuses.'''
        return {
            'method': 'GET',
            'url': f'{self.base_url}/api/UB/v1/meters/statuses'
        }

    def get_odata_UB_v1_meters_types(self):
        '''This endpoint returns meter type information.'''
        return {
            'method': 'GET',
            'url': f'{self.base_url}/odata/UB/v1/meters/types'
        }

    def get_odata_UB_v1_meters_userDefinedFieldsData(self):
        '''This endpoint returns meter custom data information.'''
        return {
            'method': 'GET',
            'url': f'{self.base_url}/odata/UB/v1/meters/userDefinedFieldsData'
        }

    def post_api_UB_v1_meters_userDefinedFieldsData(self):
        '''This endpoint creates or updates Meters user defined fields data'''
        return {
            'method': 'POST',
            'url': f'{self.base_url}/api/UB/v1/meters/userDefinedFieldsData'
        }
