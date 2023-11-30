from .base import BaseResponse


class SessionResponse(BaseResponse):
    token: str

    def __init__(self, token):
        self.token = token

    def serialize(self):
        return {"token": self.token}
