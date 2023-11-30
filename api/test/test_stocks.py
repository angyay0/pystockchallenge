import json

from flask_testing import TestCase
from api.test.test_payloads import sigup_payload
from api.test.test_utils import get_random_string

from main import api


class TestStockHandler(TestCase):
    resource = '/stocks/'
    client:any
    user:any

    def create_app(self):
        api.config.from_object("api.main.config.DevelopmentConfig")
        api.testing = True
        self.client = api.test_client()
        self.create_app_user()

        return api
    
    def create_app_user(self):
        self.user = sigup_payload()
        self.client.put('/auth/user', json=self.user)
    
    # Market symbols tests
    def test_symbols_success(self):
        token = self._get_token()
        response = self.client.get(self.resource, headers={'Authorization': 'Bearer {}'.format(token)})
        self.assert200(response)
    
    def test_symbols_query_params_success(self):
        token = self._get_token()
        query_resource = '{}?page=1&size=5'.format(self.resource)
        response = self.client.get(query_resource, headers={'Authorization': 'Bearer {}'.format(token)})
        result = json.loads(response.data.decode('utf-8'))
        self.assert200(response)
        self.assertTrue(len(result['data']) == 5)
    
    def test_symbols_expired_token(self):
        token = self._expired_token()
        response = self.client.get(self.resource, headers={'Authorization': 'Bearer {}'.format(token)})
        self.assert401(response)
    
    def _get_token(self):
        result = self.client.post('/auth/user', json=self.user)
        return json.loads(result.data.decode('utf-8'))['data']['token']
    
    def _expired_token(self):
        return 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJzdWIiOjEsImlhdCI6MTcwMTI0NDgwMiwiZXhwIjoxNzAxMjUyMDAyfQ.2fhonRGAsmI8pmfcBkUEBrAAuaGPxC2W5UpHm8H-vtb_PqD-g2UrLFlFaGms2aERL0esdnD4f2WUU7YOeFmNLw'
