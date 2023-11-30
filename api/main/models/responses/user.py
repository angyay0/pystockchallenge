from .base import BaseResponse


class UserResponse(BaseResponse):
    id: int
    email: str

    def __init__(self, id, email):
        self.email = email
        self.id = id

    # empty serialization
    def serialize(self):
        return {}
