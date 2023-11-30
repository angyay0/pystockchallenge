import json
from flask_testing import TestCase

from main import api
from api.main.models.responses.api_response import APIResponse
from api.main.models.responses.health import HealthResponse


class TestHealthNamespace(TestCase):
    healthy:APIResponse

    def create_app(self):
        self.healthy = APIResponse(0, "success", HealthResponse(0, "healthy"))
        api.config.from_object("api.main.config.DevelopmentConfig")
        api.testing = True
        return api
    
    def test_health_endpoint(self):
        response = self.app.test_client().get('/health/')
        result = json.loads(response.data.decode('utf-8'))
        self.assert200(response)
        self.assertTrue(result == self.healthy.serialize())
    
    def test_health_endpoint_fail(self):
        response = self.app.test_client().get('/health')
        self.assertStatus(response=response, status_code=308)
       
