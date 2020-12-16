import json
import os
import sys
import time

from flask import make_response

from src.flask_state.exceptions.log_msg import ErrorMsg
from src.flask_state.utils import auth, date, file_lock
from src.flask_state.utils.constants import DBAddressConstants, TimeConstants


# auth
def test_auth_method(app):
    """
    Test whether the different request types can be verified correctly
    :param app: test Flask(__name__)
    """

    @app.route("/test_method", methods=["GET", "POST"])
    @auth.auth_method
    def test_method():
        return make_response()

    c = app.test_client()
    post_response = c.post("/test_method")
    get_response = c.get("/test_method")

    ok = 200
    error = 405
    error_request_method = "Method Not Allowed"
    assert ok == post_response.status_code
    assert error == get_response.status_code
    assert error_request_method == json.loads(str(get_response.data, "utf-8")).get("msg")


# date
def test_get_current_ms():
    """
    Test whether the current MS is obtained correctly
    """

    now_ms = int(round(time.time() * TimeConstants.SECONDS_TO_MILLISECOND_MULTIPLE))
    assert now_ms == date.get_current_ms()


def test_get_current_s():
    """
    Test whether the current second is obtained correctly
    """
    now_s = int(round(time.time()))
    assert now_s == date.get_current_s()


def test_get_query_ms():
    """
    Test whether the obtained query milliseconds are correct
    """
    test_query_list = {
        1: 86400000,
        3: 259200000,
        7: 604800000,
        30: 2592000000,
        -1: 0,
        5: 0,
        14: 0,
        100: 0,
    }  # Only 1, 3, 7, 30 can be queried correctly
    for query in test_query_list:
        assert test_query_list.get(query) == date.get_query_ms(query)


# file_lock
def test_file_lock():
    """
    Test whether the file lock is successful
    """
    lock = file_lock.Lock.get_file_lock()
    lock_copy = file_lock.Lock.get_file_lock()
    assert not lock.acquire()
    try:
        lock_copy.acquire()
    except BlockingIOError as e:
        errno = 11 if os.getenv("GITHUB_ACTIONS") and sys.platform != "darwin" else 35
        assert str(e) == "[Errno {}] Resource temporarily unavailable".format(errno)

    lock.release()
    assert not lock_copy.acquire()


# format_conf
def test_format_address():
    """
    Test whether the incoming error address can throw the correct error
    """
    # key is type, value is input param
    # Test the input error type and throw the appropriate error
    target_type_error_count = 0
    min_address_length = DBAddressConstants.MIN_ADDRESS_LENGTH
    db_url_header = DBAddressConstants.DB_URL_HEADER
    test_type_list = {
        "str": "test",
        "tuple": (),
        "dict": {},
        "list": [],
        "int": 60,
        "float": 60.5,
        "bool": True,
    }  # The number of correct values is 1
    for key in test_type_list:
        try:
            if not isinstance(test_type_list.get(key), str):
                raise TypeError(
                    ErrorMsg.DATA_TYPE_ERROR.get_msg(
                        ". The target type is {}, not {}".format(str.__name__, type(test_type_list.get(key)).__name__)
                    )
                )
        except TypeError as t:
            target_type_error_count += 1
            assert t.__str__() == "Data type format error. The target type is str, not %s" % key
            assert isinstance(t, TypeError)
    assert target_type_error_count == len(test_type_list) - 1

    # sqlite test url
    # Test whether the correct SQLite URL can be detected
    target_address_error_count = 0
    test_address_list = [
        "test.db",
        "sqi:test.db",
        "sqlte:///test.db",
        "sqlite:///",
        "sqlite://test.db",
        "sqlite:///test.db",
    ]  # The number of correct values is 1
    for address in test_address_list:
        try:
            if len(address) < min_address_length or address[: min_address_length - 1] != db_url_header:
                raise ValueError(ErrorMsg.ERROR_ADDRESS.get_msg(". Error Sqlite url: %s" % address))
        except ValueError as v:
            target_address_error_count += 1
            assert (
                v.__str__()
                == "Incorrect address format, Set the format to: sqlite:///path. Error Sqlite url: %s" % address
            )
    assert target_address_error_count == len(test_address_list) - 1

    correct_address_list = ["sqlite:///test.db", "sqlite:////"]
    for address in correct_address_list:
        index = address[min_address_length - 1 :].rfind("/")
        address_path = address[min_address_length - 1 :][:index] if index != -1 else "./"
        try:
            if not os.access(address_path, os.W_OK):
                raise ValueError(ErrorMsg.NO_ACCESS.get_msg(". No access path: %s" % address))
        except ValueError as v:
            assert (
                v.__str__() == "Path has no access, make sure you have access to the path. No access path: %s" % address
            )
