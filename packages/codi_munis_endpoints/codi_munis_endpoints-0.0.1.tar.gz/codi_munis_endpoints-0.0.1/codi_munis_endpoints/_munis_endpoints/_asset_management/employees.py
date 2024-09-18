from yarl import URL


class Employees:
    def __init__(self, base_url):
        self.base_url = base_url
        self.prefix_url = "Prod/munisopenapi/hosts/EAM/"
    
    @property
    def url(self):
        base_url = URL(self.base_url)
        return base_url / self.prefix_url


    def get_odata_HR_v2_employees(self):
        '''This endpoint returns employee information'''
        return {
            'method': 'GET',
            'url': str(self.url / 'odata/HR/v2/employees')
        }

    def get_api_HR_v1_employees_schedule(self, employeeNumber):
        '''This endpoint gets employee schedule information.'''
        return {
            'method': 'GET',
            'url': str(self.url / f'api/HR/v1/employees/{employeeNumber}/schedule')
        }

    def get_odata_HR_v2_employees_certifications(self):
        '''This endpoint returns all certifications for an employee'''
        return {
            'method': 'GET',
            'url': str(self.url / 'odata/HR/v2/employees/certifications')
        }

    def get_api_PR_v1_employees_hoursWorked(self):
        '''This endpoint gets hours worked for an employee.'''
        return {
            'method': 'GET',
            'url':str(self.url / 'api/PR/v1/employees/hoursWorked')
        }

    def post_api_PR_v1_employees_hoursWorked(self):
        '''This endpoint posts hours worked for an employee.'''
        return {
            'method': 'POST',
            'url':str(self.url / 'api/PR/v1/employees/hoursWorked')
        }

    def put_api_PR_v1_employees_hoursWorked(self):
        '''This endpoint updates hours worked for an employee.'''
        return {
            'method': 'PUT',
            'url':str(self.url / 'api/PR/v1/employees/hoursWorked')
        }

    def get_odata_PR_v2_employees_laborRates(self):
        '''This endpoint returns employee labor rate information'''
        return {
            'method': 'GET',
            'url':str(self.url / 'odata/PR/v2/employees/laborRates')
        }
