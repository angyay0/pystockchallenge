from flask import request
from flask_restplus import Resource

from api.main.models.responses.api_response import APIResponse
from api.main.utils.definitions import HealthDefinition
from api.main.handlers.health import get_health

health_api = HealthDefinition.api


@health_api.route("/")
class GetHealth(Resource):
    @health_api.response(200, "Success")
    @health_api.doc("Get Health")
    def get(self):
        return get_health().serialize()
