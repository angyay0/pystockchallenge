from .base import BaseResponse


class GenericResponse(BaseResponse):
    message: str
    done: bool

    def __init__(self, done, message):
        self.done = done
        self.message = message

    def serialize(self):
        return {"done": self.done, "message": self.message}
