class Generalledgercodes:
    def __init__(self, base_url):
        self.base_url = base_url

    def get_odata_GL_v1_generalLedgerCodes_reasonCodes(self):
        '''This endpoint returns general ledger code reason code information'''
        return {
            'method': 'GET',
            'url': f'{self.base_url}/odata/GL/v1/generalLedgerCodes/reasonCodes'
        }

    def get_odata_GL_v1_generalLedgerCodes_responsibilityCodes(self):
        '''This endpoint returns general ledger code responsibility code information'''
        return {
            'method': 'GET',
            'url': f'{self.base_url}/odata/GL/v1/generalLedgerCodes/responsibilityCodes'
        }
