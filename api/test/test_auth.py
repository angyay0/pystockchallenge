import json
import os
from flask_testing import TestCase
from api.test.test_utils import get_random_string

from main import api

class TestAuthHandler(TestCase):
    resource = '/auth/user'
    client:any

    def create_app(self):
        api.config.from_object("api.main.config.DevelopmentConfig")
        api.testing = True
        self.client = api.test_client()
        return api
    
    # Login Tests
    def test_login_success(self):
        response = self._do_login(self._login_payload())
        result = json.loads(response.data.decode('utf-8'))
        self.assert200(response)
        self.assertTrue(result['code'] == 0)
        self.assertTrue(result['message'] == 'Sucessful Login')
        self.assertTrue(result['data']['token'] != None)
    
    def test_login_failed(self):
        response = self._do_login({})
        self.assert400(response)
    
    def test_login_incomplete_payload(self):
        response = self._do_login({'email': 'test@mail.com'})
        self.assert400(response)
    
    #OTP Flow
    def test_otp_success(self):
        payload = self._sigup_payload(otp=True, rand=get_random_string(4))
        self.client.put(self.resource, json=payload)
        pre_login = self.client.post(self.resource, json=payload)
        pre_login_result = json.loads(pre_login.data.decode('utf-8'))
        otp_code = os.getenv('OTP_TESTING_CODE') or '000000'
        self.assert200(pre_login)
        self.assertTrue(pre_login_result['code'] == 1)
        session = self.client.post('{}/tfa'.format(self.resource), json={
            "token": pre_login_result['data']['token'],
            "code": otp_code
        })
        result = json.loads(session.data.decode('utf-8'))
        self.assert200(session)
        self.assertTrue(result['code'] == 0)
        self.assertTrue(result['message'] == 'Sucessful Login')
    
    def test_otp_mismatch(self):
        payload = self._sigup_payload(otp=True, rand=get_random_string(4))
        self.client.put(self.resource, json=payload)
        pre_login = self.client.post(self.resource, json=payload)
        pre_login_result = json.loads(pre_login.data.decode('utf-8'))
        otp_code = '000000'
        self.assert200(pre_login)
        self.assertTrue(pre_login_result['code'] == 1)
        session = self.client.post('{}/tfa'.format(self.resource), json={
            "token": pre_login_result['data']['token'],
            "code": otp_code
        })
        result = json.loads(session.data.decode('utf-8'))
        self.assert400(session)
        self.assertTrue(result['data']['message'] == 'CodeMismatch')
    
    def test_otp_failed(self):
        payload = self._sigup_payload(otp=True, rand=get_random_string(4))
        self.client.put(self.resource, json=payload)
        pre_login = self.client.post(self.resource, json=payload)
        pre_login_result = json.loads(pre_login.data.decode('utf-8'))
        otp_code = '000000'
        self.assert200(pre_login)
        self.assertTrue(pre_login_result['code'] == 1)
        session = self.client.post('{}/tfa'.format(self.resource), json={
            "token": otp_code,
            "code": otp_code
        })
        result = json.loads(session.data.decode('utf-8'))
        self.assert400(session)
        self.assertTrue(result['data']['message'] == 'ExpiredTokenOrInvalidOTP')

    
    # Sign up Tests
    def test_signup_failed(self):
        response = self.client.put(self.resource, json={})
        result= json.loads(response.data.decode('utf-8'))
        self.assert400(response)
        self.assertTrue('errors' in result.keys())
    
    def test_signup_incomplete_fields(self):
        payload = self._sigup_payload()
        payload.pop("email")
        response = self.client.put(self.resource, json=payload)
        self.assert400(response)
    
    def test_signup_duplicated_fail(self):
        payload = self._sigup_payload()
        payload['email'] = 'test@mail.com'
        response = self.client.put(self.resource, json=payload)
        result= json.loads(response.data.decode('utf-8'))
        self.assert400(response)
        self.assertTrue(result['code'] == -1)
        self.assertFalse(result['data']['done'])
        self.assertTrue(result['data']['message'] == 'CannotRegister')
    
    def test_signup_success(self):
        payload = self._sigup_payload(rand=get_random_string(8))
        response = self.client.put(self.resource, json=payload)
        result = json.loads(response.data.decode('utf-8'))
        self.assert200(response)
        self.assertTrue(result['code'] == 0)
        self.assertTrue(result['message'] == 'Success')
        self.assertTrue(result['data']['message'] == 'Completed')
        self.assertTrue(result['data']['done'])
    
    # Edit Tests
    def test_edit_expired_token(self):
        edit_result = self.client.patch(self.resource, 
            json=self._sigup_payload(), 
            headers={'Authorization': 'Bearer {}'.format(self._expired_token())
        })
        self.assert401(edit_result)

    def test_edit_success(self):
        payload = self._sigup_payload(rand=get_random_string(6))
        self.client.put(self.resource, json=payload)
        login_result = self.client.post(self.resource, json=payload)
        credentials = json.loads(login_result.data.decode('utf-8'))
        self.assert200(login_result)
        payload['name'] = 'Testbert'
        edit_response = self.client.patch(self.resource, json=payload, headers={
            'Authorization': 'Bearer {}'.format(credentials['data']['token'])
        })
        edit_result = json.loads(edit_response.data.decode('utf-8'))
        self.assert200(edit_response)
        self.assertTrue(edit_result['code'] == 0)
        self.assertTrue(edit_result['message'] == 'Success')

    # Delete Tests
    def test_delete_no_token(self):
        response = self.client.delete(self.resource)
        self.assert401(response)
    
    def test_delete_expired_token(self):
        response = self.client.delete(self.resource, headers={'Authorization': 'Bearer {}'.format(self._expired_token())})
        self.assert401(response)
    
    def test_delete_success(self):
        payload = self._sigup_payload(rand=get_random_string(8))
        self.client.put(self.resource, json=payload)
        response = self.client.post(self.resource, json=payload)
        result = json.loads(response.data.decode('utf-8'))
        self.assert200(response)
        delete_response = self.client.delete(self.resource,  headers={'Authorization': 'Bearer {}'.format(result['data']['token'])})
        self.assert200(delete_response)
    
    def _do_login(self, payload):
        return self.client.post(self.resource, json=payload)
    
    def _login_payload(self):
        return {
            "email": "test@mail.com",
            "password": "Testing1"
        }
    
    def _sigup_payload(self, otp=False, rand=''):
        return {
            "email": "tester{}@test.com".format(rand),
            "password": "Testing1",
            "name": "Test",
            "last_name": "Test",
            "phone_number": "1234123456",
            "otp": otp
        }
    
    def _otp_payload(self, token=''):
        return {
            "token": token,
            "code": '00000'
        }
    
    def _expired_token(self):
        return 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJzdWIiOjEsImlhdCI6MTcwMTI0NDgwMiwiZXhwIjoxNzAxMjUyMDAyfQ.2fhonRGAsmI8pmfcBkUEBrAAuaGPxC2W5UpHm8H-vtb_PqD-g2UrLFlFaGms2aERL0esdnD4f2WUU7YOeFmNLw'