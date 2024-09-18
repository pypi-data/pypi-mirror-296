class Accounts:
    def __init__(self, base_url):
        self.base_url = base_url

    def get_odata_GL_v1_accounts(self):
        '''This endpoint returns general ledger account information.'''
        return {
            'method': 'GET',
            'url': f'{self.base_url}/odata/GL/v1/accounts'
        }

    def get_odata_GL_v1_accounts_xref(self):
        '''This endpoint returns general ledger account information.'''
        return {
            'method': 'GET',
            'url': f'{self.base_url}/odata/GL/v1/accounts/xref'
        }
