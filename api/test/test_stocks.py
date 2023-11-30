import json

from flask_testing import TestCase
from api.test.test_payloads import sigup_payload

from main import api


class TestStockHandler(TestCase):
    resource = "/stocks"
    client: any
    userPayload: any

    def create_app(self):
        api.config.from_object("api.main.config.DevelopmentConfig")
        api.testing = True
        self.client = api.test_client()
        self.userPayload = sigup_payload()
        self.client.put("/auth/user", json=self.userPayload)
        token = self._get_token(self.userPayload)
        self.client.put(
            "{}/portfolio".format(self.resource),
            json={"symbol": "AAA"},
            headers={"Authorization": "Bearer {}".format(token)},
        )
        self.client.put(
            "{}/portfolio".format(self.resource),
            json={"symbol": "AA"},
            headers={"Authorization": "Bearer {}".format(token)},
        )

        return api

    # Market symbols tests
    def test_symbols_success(self):
        token = self._get_token(self.userPayload)
        response = self.client.get(
            "{}/".format(self.resource),
            headers={"Authorization": "Bearer {}".format(token)},
        )
        self.assert200(response)

    def test_symbols_params_success(self):
        token = self._get_token(self.userPayload)
        response = self.client.get(
            "{}/?size=5&page=1".format(self.resource),
            headers={"Authorization": "Bearer {}".format(token)},
        )
        result = json.loads(response.data.decode("utf-8"))
        self.assert200(response)
        self.assertTrue(result["code"] == 0)
        self.assertTrue(len(result["data"]) == 5)

    def test_symbols_expired_token(self):
        token = self._expired_token()
        response = self.client.get(
            self.resource + "/", headers={"Authorization": "Bearer {}".format(token)}
        )
        self.assert401(response)

    # Portfolio Tests
    def test_get_portfolio(self):
        token = self._get_token(self.userPayload)
        response = self.client.get(
            "{}/portfolio".format(self.resource),
            headers={"Authorization": "Bearer {}".format(token)},
        )
        result = json.loads(response.data.decode("utf-8"))
        self.assert200(response)
        self.assertTrue(result["code"] == 0)
        self.assertTrue(len(result["data"]) > 0)

    def test_add_to_portfolio_success(self):
        token = self._get_token(self.userPayload)
        response = self.client.put(
            "{}/portfolio".format(self.resource),
            json={"symbol": "A"},
            headers={"Authorization": "Bearer {}".format(token)},
        )
        result = json.loads(response.data.decode("utf-8"))
        self.assert200(response)
        self.assertTrue(result["code"] == 0)
        self.assertTrue(result["data"])

    def test_add_to_portfolio_duplicated(self):
        token = self._get_token(self.userPayload)
        response = self.client.put(
            "{}/portfolio".format(self.resource),
            json={"symbol": "AAA"},
            headers={"Authorization": "Bearer {}".format(token)},
        )
        result = json.loads(response.data.decode("utf-8"))
        self.assert400(response)
        self.assertTrue(result["code"] == 2)
        self.assertTrue(result["message"] == "Already in Portfolio")

    def test_add_to_portfolio_fail(self):
        token = self._get_token(self.userPayload)
        response = self.client.put(
            "{}/portfolio".format(self.resource),
            json={"symbol": "NOEXISTS"},
            headers={"Authorization": "Bearer {}".format(token)},
        )
        result = json.loads(response.data.decode("utf-8"))
        self.assert400(response)
        self.assertTrue(result["code"] == -1)
        self.assertFalse(result["data"])
        self.assertTrue(result["message"] == "Symbol is not tracked")

    def test_delete_from_portfolio_success(self):
        token = self._get_token(self.userPayload)
        response = self.client.delete(
            "{}/portfolio".format(self.resource),
            json={"symbol": "AA"},
            headers={"Authorization": "Bearer {}".format(token)},
        )
        result = json.loads(response.data.decode("utf-8"))
        self.assert200(response)
        self.assertTrue(result["code"] == 0)
        self.assertTrue(result["data"])

    def test_delete_from_portfolio_failed(self):
        token = self._get_token(self.userPayload)
        response = self.client.delete(
            "{}/portfolio".format(self.resource),
            json={"symbol": "NOEXISTS"},
            headers={"Authorization": "Bearer {}".format(token)},
        )
        result = json.loads(response.data.decode("utf-8"))
        self.assert400(response)
        self.assertTrue(result["code"] == -1)
        self.assertFalse(result["data"])

    # Analytics Tests
    def test_get_analytics(self):
        token = self._get_token(self.userPayload)
        response = self.client.get(
            "{}/analytics".format(self.resource),
            headers={"Authorization": "Bearer {}".format(token)},
        )
        result = json.loads(response.data.decode("utf-8"))
        self.assert200(response)
        self.assertTrue(result["code"] == 0)
        self.assertTrue(len(result["data"]) > 0)

    def test_add_analytics_success(self):
        token = self._get_token(self.userPayload)
        payload = {"symbol": "AA", "analytic": "SMA"}
        response = self.client.put(
            "{}/analytics".format(self.resource),
            json=payload,
            headers={"Authorization": "Bearer {}".format(token)},
        )
        result = json.loads(response.data.decode("utf-8"))
        self.assert200(response)
        self.assertTrue(result["code"] == 0)
        self.assertTrue(result["data"])

    def test_add_analytics_failed(self):
        token = self._get_token(self.userPayload)
        payload = {"symbol": "AA", "analytic": "NOTVALID"}
        response = self.client.put(
            "{}/analytics".format(self.resource),
            json=payload,
            headers={"Authorization": "Bearer {}".format(token)},
        )
        result = json.loads(response.data.decode("utf-8"))
        self.assert400(response)
        self.assertTrue(result["code"] == -1)
        self.assertFalse(result["data"])

    def test_add_analytics_duplicated(self):
        token = self._get_token(self.userPayload)
        payload = {"symbol": "AA", "analytic": "EMA"}
        self.client.put(
            "{}/analytics".format(self.resource),
            json=payload,
            headers={"Authorization": "Bearer {}".format(token)},
        )
        response = self.client.put(
            "{}/analytics".format(self.resource),
            json=payload,
            headers={"Authorization": "Bearer {}".format(token)},
        )
        result = json.loads(response.data.decode("utf-8"))
        self.assert400(response)
        self.assertTrue(result["code"] == -1)
        self.assertFalse(result["data"])

    def test_delete_analytics_success(self):
        token = self._get_token(self.userPayload)
        payload = {"symbol": "AA", "analytic": "ADA"}
        self.client.put(
            "{}/analytics".format(self.resource),
            json=payload,
            headers={"Authorization": "Bearer {}".format(token)},
        )
        response = self.client.delete(
            "{}/analytics".format(self.resource),
            json=payload,
            headers={"Authorization": "Bearer {}".format(token)},
        )
        result = json.loads(response.data.decode("utf-8"))
        self.assert200(response)
        self.assertTrue(result["code"] == 0)
        self.assertTrue(result["data"])

    def _get_token(self, payload):
        result = self.client.post("/auth/user", json=payload)
        res = json.loads(result.data.decode("utf-8"))
        return res["data"]["token"]

    def _expired_token(self):
        return "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJzdWIiOjEsImlhdCI6MTcwMTI0NDgwMiwiZXhwIjoxNzAxMjUyMDAyfQ.2fhonRGAsmI8pmfcBkUEBrAAuaGPxC2W5UpHm8H-vtb_PqD-g2UrLFlFaGms2aERL0esdnD4f2WUU7YOeFmNLw"
