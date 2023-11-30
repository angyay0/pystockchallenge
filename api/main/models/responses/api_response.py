from .base import BaseResponse


class APIResponse(BaseResponse):
    code: int
    message: str
    data: None

    def __init__(self, code, message, data):
        self.code = code
        self.message = message
        self.data = data

    def serialize(self):
        return {
            "code": self.code,
            "message": self.message,
            "data": self.serialize_data(),
        }

    def serialize_data(self):
        if type(self.data) == list:
            serialized = []
            for item in list(self.data):
                if str(item.__class__).__contains__("Response"):
                    serialized.append(item.serialize())
                else:
                    serialized.append(item)

            return serialized
        elif str(self.data.__class__).__contains__("Response"):
            return self.data.serialize()
        else:
            return self.data


class APIResponsePaged(APIResponse):
    page: int
    next: str
    prev: str

    def __init__(
        self,
        code,
        message,
        data,
        page,
        next=None,
        prev=None,
    ):
        self.code = code
        self.message = message
        self.data = data
        self.page = page
        self.next = next
        self.prev = prev

    def serialize(self):
        return {
            "code": self.code,
            "message": self.message,
            "paged": {"page": self.page, "next": self.next, "prev": self.prev},
            "data": self.serialize_data(),
        }
