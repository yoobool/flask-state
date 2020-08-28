from flask_state.utils import date, file_lock, format_conf, auth
import time


def test_get_current_ms():
    dv = date.get_current_ms() - int(round(time.time() * 1000))
    assert -100 < dv < 100


def test_get_current_s():
    dv = date.get_current_s() - int(round(time.time()))
    assert dv == 0


def test_get_query_ms():
    assert date.get_query_ms('1') == 86400000
    assert date.get_query_ms('3') == 259200000
    assert date.get_query_ms('7') == 604800000
    assert date.get_query_ms('30') == 2592000000

    # Boundary values and different types of tests
    assert date.get_query_ms(0) == 0
    assert date.get_query_ms('a') == 0
    assert date.get_query_ms([]) == 0
    assert date.get_query_ms({}) == 0
    assert date.get_query_ms((1, 0)) == 0


def test_file_lock():
    lock = file_lock.Lock.get_file_lock()
    lock_copy = file_lock.Lock.get_file_lock()

    assert not lock.acquire()
    try:
        lock_copy.acquire()
    except Exception as e:
        assert str(e) == "[Errno 35] Resource temporarily unavailable"

    lock.release()
    assert not lock_copy.acquire()


def test_format_conf():
    fl = format_conf.format_language()
    fa = format_conf.format_address()
    fi = format_conf.format_id_name()
    fs = format_conf.format_sec()

    assert isinstance(fl, str)
    assert isinstance(fa, str)
    assert isinstance(fi, tuple)
    assert isinstance(fs, int)


def test_auth_user():
    def func():
        return True
    assert auth.auth_user(func)
