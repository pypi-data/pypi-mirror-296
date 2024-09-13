from logging import Logger
import requests
from halo import Halo

class ProjectApiError(Exception):
    def __init__(self, message: str, code: str):            
        super().__init__(message)
        self.code = code
   

class ProjectApi: 
    __SERVER_URL = 'https://wake-arena-project-api-1076910080992.europe-west3.run.app'

    def __init__(self, logger: Logger, client_id: str, token: str):
        self.logger = logger
        self.client_id = client_id
        self.token = token
        self.headers = {
            'Authorization': f'Bearer {token}',
            'X-Client-Id': str(client_id),
        }

    def __check_response(self, res, body):
        if res.status_code != 200:
            print(body)
            code = body['code']
            self.logger.error(f"Wake Arena Project API error: {res.status_code}")
            self.logger.error(f"{code}")
            raise ProjectApiError(f"Wake Arena Project API error: {res.status_code}", code)

    @Halo(text='Creating project', spinner='dots')
    def create_project(self, project_name: str):
        body = {
            'name': project_name
        }
        res = requests.post(self.__SERVER_URL + '/api/v0/projects', json=body, headers=self.headers)
        body = res.json()

        self.__check_response(res, body)

        return body
    
    @Halo(text='Initializing upload', spinner='dots')
    def get_upload_link(self, project_id: str):
        res = requests.post(self.__SERVER_URL + f'/api/v0/projects/{project_id}/code-upload', headers=self.headers)
        body = res.json()

        self.__check_response(res, body)

        return body