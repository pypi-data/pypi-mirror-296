from .employees import Employees

class AssetManagement:
    def __init__(self, base_url):
        self.base_url = base_url
        self.employees = Employees(base_url)