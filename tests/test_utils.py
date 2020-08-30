import time
from flask_state.utils import date, file_lock, format_conf, auth


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
    try:
        format_conf.format_language()
    except TypeError as t:
        assert isinstance(t, TypeError)
    fl = format_conf.format_language(123)
    assert isinstance(fl, str)
    fl = format_conf.format_language(None)
    assert isinstance(fl, str)
    fl = format_conf.format_language(True)
    assert isinstance(fl, str)

    try:
        format_conf.format_address()
    except TypeError as t:
        assert isinstance(t, TypeError)
    fa = format_conf.format_address('asd?')
    assert fa == 'sqlite:///asd?'
    fa = format_conf.format_address('aa/aa/a?a/aas?d')
    assert fa == 'sqlite:///./'
    fa = format_conf.format_address('!asd')
    assert fa == 'sqlite:///!asd'
    fa = format_conf.format_address('asdd/d')
    assert fa == 'sqlite:///./'

    try:
        format_conf.format_id_name()
    except TypeError as t:
        assert isinstance(t, TypeError)
    fi = format_conf.format_id_name(True, 'asdsa')
    assert fi == ('True', True)
    fi = format_conf.format_id_name(None, 'asd')
    assert fi == ('None', True)
    fi = format_conf.format_id_name('asd')
    assert fi == ('asd', True)
    fi = format_conf.format_id_name('asd', 'asd')
    assert fi == ('asd', True)

    try:
        format_conf.format_sec()
    except TypeError as t:
        assert isinstance(t, TypeError)
    fs = format_conf.format_sec('123123')
    assert fs == 60
    fs = format_conf.format_sec(True)
    assert fs == 60
    fs = format_conf.format_sec(None)
    assert fs == 60
    fs = format_conf.format_sec(-1)
    assert fs == 60
    fs = format_conf.format_sec(100)
    assert fs == 100
    fs = format_conf.format_sec(50)
    assert fs == 50


def test_auth_user():
    def func():
        return True

    assert auth.auth_user(func)
