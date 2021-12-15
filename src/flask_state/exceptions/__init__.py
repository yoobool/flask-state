from abc import ABC, abstractmethod
from enum import Enum, unique


class FlaskStateResponse(ABC):
    @abstractmethod
    def get_code(self):
        raise NotImplementedError("get_code() not implemented")

    @abstractmethod
    def get_msg(self):
        raise NotImplementedError("get_msg() not implemented")

    @abstractmethod
    def get_data(self):
        raise NotImplementedError("get_data() not implemented")


# Success response
class SuccessResponse(FlaskStateResponse):
    def __init__(self, msg=None, data=None):
        if msg is None:
            msg = "SUCCESS"
        self.code = 200
        self.msg = msg
        self.data = data

    def get_code(self):
        return self.code

    def get_msg(self):
        return self.msg

    def get_data(self):
        return self.data


# Enumeration function
@unique
class ErrorCode(Enum):
    def get_code(self):
        return self.value.get("code")

    def get_msg(self):
        return self.value.get("msg")


@unique
class ExceptionMsg(Enum):
    def get_level(self):
        return self.value.get("level")

    def get_msg(self, supplement=""):
        return self.value.get("msg") + supplement


class FlaskException(Exception):
    status_code = 400

    def __init__(
        self, error_message: ErrorCode, status_code=None, payload=None
    ):
        Exception.__init__(self)
        self.message = error_message.get_msg()
        self.code = error_message.get_code()
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv["msg"] = self.message
        rv["code"] = self.code
        return rv

    def __str__(self):
        return "{}: ({}) {!r} {!r}".format(
            self.__class__.__name__,
            self.status_code,
            self.code,
            self.message,
        )
