class Accountsreceivablecodes:
    def __init__(self, base_url):
        self.base_url = base_url

    def get_odata_AR_v1_accountsReceivableCodes(self):
        '''This endpoint returns AR codes information'''
        return {
            'method': 'GET',
            'url': f'{self.base_url}/odata/AR/v1/accountsReceivableCodes'
        }
