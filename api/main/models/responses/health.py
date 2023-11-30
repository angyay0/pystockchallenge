from .base import BaseResponse


class HealthResponse(BaseResponse):
    code: int
    status: str

    def __init__(self, code, status):
        self.code = code
        self.status = status

    def serialize(self):
        return {"code": self.code, "status": self.status}
