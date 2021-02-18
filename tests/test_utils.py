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
