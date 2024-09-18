class Vendors:
    def __init__(self, base_url):
        self.base_url = base_url

    def get_odata_AP_v1_contactTypes(self):
        '''This endpoint returns contact types information.'''
        return {
            'method': 'GET',
            'url': f'{self.base_url}/odata/AP/v1/contactTypes'
        }

    def get_odata_AP_v1_mbeClassifications(self):
        '''This endpoint returns MBEClassification information.'''
        return {
            'method': 'GET',
            'url': f'{self.base_url}/odata/AP/v1/mbeClassifications'
        }

    def get_odata_AP_v1_vendorRemittanceTypes(self):
        '''This endpoint returns vendor remittance type information.'''
        return {
            'method': 'GET',
            'url': f'{self.base_url}/odata/AP/v1/vendorRemittanceTypes'
        }

    def get_odata_AP_v1_vendors(self):
        '''This endpoint returns vendor information.'''
        return {
            'method': 'GET',
            'url': f'{self.base_url}/odata/AP/v1/vendors'
        }

    def get_odata_AP_v2_vendors(self):
        '''This endpoint returns vendor information.'''
        return {
            'method': 'GET',
            'url': f'{self.base_url}/odata/AP/v2/vendors'
        }

    def get_odata_AP_v2_vendors_contacts(self):
        '''This endpoint returns vendor information.'''
        return {
            'method': 'GET',
            'url': f'{self.base_url}/odata/AP/v2/vendors/contacts'
        }

    def get_odata_AP_v1_vendors_statusCodes(self):
        '''This endpoint returns vendor status codes information.'''
        return {
            'method': 'GET',
            'url': f'{self.base_url}/odata/AP/v1/vendors/statusCodes'
        }

    def get_odata_AP_v2_vendors_vendorRemittances(self):
        '''This endpoint returns vendor information.'''
        return {
            'method': 'GET',
            'url': f'{self.base_url}/odata/AP/v2/vendors/vendorRemittances'
        }
