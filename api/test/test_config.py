import os
import unittest

from flask import current_app
from flask_testing import TestCase

from main import api
from api.main.config import basedir


class TestDevelopmentConfig(TestCase):
    def create_app(self):
        api.config.from_object("api.main.config.DevelopmentConfig")
        return api

    def test_app_is_development(self):
        self.assertFalse(api.config["SECRET_KEY"] == "__SECRET_KEY__")
        self.assertTrue(api.config["DEBUG"] == True)
        self.assertFalse(current_app == None)


class TestProductionConfig(TestCase):
    def create_app(self):
        api.config.from_object("api.main.config.ProductionConfig")
        return api

    def test_app_is_production(self):
        self.assertTrue(api.config["DEBUG"] == False)


if __name__ == "__main__":
    unittest.main()
