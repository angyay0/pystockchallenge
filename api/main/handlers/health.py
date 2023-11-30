from api.main.models.responses.health import HealthResponse
from api.main.models.responses.api_response import APIResponse


def get_health():
    """Get API Health"""
    return APIResponse(0, "success", HealthResponse(0, "healthy"))
