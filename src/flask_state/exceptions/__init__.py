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


# Error response
class ErrorResponse(FlaskStateResponse):
    def __init__(self, error_code):
        self.error_code = error_code
        self.data = []

    def get_code(self):
        return self.error_code.get_code()

    def get_msg(self):
        return self.error_code.get_msg()

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


class FlaskStateError(Exception):
    def __init__(self, *args, **kwargs):
        """
        :param int status_code: standard http status code use by FlaskState
        :param str msg:
        """
        super(FlaskStateError, self).__init__()
        self.status_code = int(kwargs.get("status_code"))
        self.msg = str(kwargs.get("msg"))
        self.reply_code = kwargs.get("code", self.status_code)
        self.data = []

    def get_msg(self):
        return self.msg

    def get_code(self):
        return self.reply_code

    def get_data(self):
        return self.data

    def __repr__(self):
        return "{}: ({}) {!r} {!r}".format(
            self.__class__.__name__,
            self.status_code,
            self.reply_code,
            self.msg,
        )
