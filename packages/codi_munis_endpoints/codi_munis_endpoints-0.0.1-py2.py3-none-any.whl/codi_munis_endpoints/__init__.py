"""
Munis Endpoints
"""
__version__ = "0.0.1"

from ._munis_endpoints import _asset_management

class MunisEndpoints:
    def __init__(self, base_url):
        self.base_url = base_url
        self.asset_management = _asset_management.AssetManagement(base_url)

