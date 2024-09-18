class Flatinventory:
    def __init__(self, base_url):
        self.base_url = base_url

    def get_odata_UB_v1_flatInventory(self):
        '''This endpoint returns flat inventory information.'''
        return {
            'method': 'GET',
            'url': f'{self.base_url}/odata/UB/v1/flatInventory'
        }

    def get_odata_UB_v2_flatInventory(self):
        '''This endpoint returns flat inventory information.'''
        return {
            'method': 'GET',
            'url': f'{self.base_url}/odata/UB/v2/flatInventory'
        }

    def post_api_UB_v1_flatInventory(self):
        '''This endpoint creates a UB flat inventory.'''
        return {
            'method': 'POST',
            'url': f'{self.base_url}/api/UB/v1/flatInventory'
        }

    def put_api_UB_v1_flatInventory(self):
        '''This endpoint updates UB flat inventory.'''
        return {
            'method': 'PUT',
            'url': f'{self.base_url}/api/UB/v1/flatInventory'
        }

    def get_odata_UB_v1_flatInventory_conditionCodes(self):
        '''This endpoint returns flat inventory condition code information.'''
        return {
            'method': 'GET',
            'url': f'{self.base_url}/odata/UB/v1/flatInventory/conditionCodes'
        }

    def get_odata_UB_v1_flatInventory_itemCodes(self):
        '''This endpoint returns flat inventory item code information.'''
        return {
            'method': 'GET',
            'url': f'{self.base_url}/odata/UB/v1/flatInventory/itemCodes'
        }

    def get_odata_UB_v1_flatInventory_manufacturerCodes(self):
        '''This endpoint returns flat inventory manufacturer code information.'''
        return {
            'method': 'GET',
            'url': f'{self.base_url}/odata/UB/v1/flatInventory/manufacturerCodes'
        }

    def get_odata_UB_v1_flatInventory_modelCodes(self):
        '''This endpoint returns flat inventory model code information.'''
        return {
            'method': 'GET',
            'url': f'{self.base_url}/odata/UB/v1/flatInventory/modelCodes'
        }

    def get_odata_UB_v1_flatInventory_userDefinedFieldsData(self):
        '''This endpoint returns flat inventory custom data information.'''
        return {
            'method': 'GET',
            'url': f'{self.base_url}/odata/UB/v1/flatInventory/userDefinedFieldsData'
        }

    def post_api_UB_v1_flatInventory_userDefinedFieldsData(self):
        '''This endpoint creates or updates flat inventory user defined fields data'''
        return {
            'method': 'POST',
            'url': f'{self.base_url}/api/UB/v1/flatInventory/userDefinedFieldsData'
        }

    def get_odata_UB_v1_flatInventory_weightDescriptionCodes(self):
        '''This endpoint returns flat inventory weight description code information.'''
        return {
            'method': 'GET',
            'url': f'{self.base_url}/odata/UB/v1/flatInventory/weightDescriptionCodes'
        }
