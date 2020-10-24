import os

from src.flask_state.conf.config import Constant
from src.flask_state.exceptions.log_msg import ErrorMsg
from src.flask_state.utils import format_conf


# format_conf
def test_format_sec():
    """
    Test whether the error in the number of seconds passed in is thrown normally,
    and whether the number of seconds is returned correctly
    """
    # key is type, value is input param
    # Test the input error type and throw the appropriate error
    target_type_error_count = 0
    test_type_list = {'str': 'test', 'tuple': tuple(), 'dict': dict(), 'list': list(), 'int': 60, 'float': 60.5,
                      'bool': True}  # The number of correct values is 2, bool is treated as int
    for key in test_type_list:
        try:
            format_conf.format_sec(test_type_list.get(key))
        except TypeError as t:
            target_type_error_count += 1
            assert t.__str__() == 'Data type format error. The target type is int, not %s' % key
            assert isinstance(t, TypeError)
    assert target_type_error_count == len(test_type_list) - 2

    # key is input, value is correct output
    # Test whether the correct number of seconds can be returned
    test_seconds_list = {-100: 60, 0: 60, 10: 60, 50: 60, 60: 60, 100: 100,
                         10000: 10000}  # The number of correct values is 3
    for key in test_seconds_list:
        assert test_seconds_list.get(key) == format_conf.format_sec(key)


def test_format_address():
    """
    Test whether the incoming error address can throw the correct error
    """
    # key is type, value is input param
    # Test the input error type and throw the appropriate error
    target_type_error_count = 0
    test_type_list = {'str': 'test', 'tuple': tuple(), 'dict': dict(), 'list': list(), 'int': 60, 'float': 60.5,
                      'bool': True}  # The number of correct values is 1
    for key in test_type_list:
        try:
            if not isinstance(test_type_list.get(key), str):
                raise TypeError(
                    ErrorMsg.DATA_TYPE_ERROR.get_msg(
                        '. The target type is %s, not %s' % (str.__name__, type(test_type_list.get(key)).__name__)))
        except TypeError as t:
            target_type_error_count += 1
            assert t.__str__() == 'Data type format error. The target type is str, not %s' % key
            assert isinstance(t, TypeError)
    assert target_type_error_count == len(test_type_list) - 1

    # sqlite test url
    # Test whether the correct SQLite URL can be detected
    target_address_error_count = 0
    test_address_list = ['test.db', 'sqi:test.db', 'sqlte:///test.db', 'sqlite:///', 'sqlite://test.db',
                         'sqlite:///test.db']  # The number of correct values is 1
    for address in test_address_list:
        try:
            if len(address) < Constant.MIN_ADDRESS_LENGTH \
                    or address[:Constant.MIN_ADDRESS_LENGTH - 1] != format_conf.DB_URL_HEADER:
                raise ValueError(ErrorMsg.ERROR_ADDRESS.get_msg('. Error Sqlite url: %s' % address))
        except ValueError as v:
            target_address_error_count += 1
            assert v.__str__() == 'Incorrect address format, Set the format to: sqlite:///path. Error Sqlite url: %s' % address
    assert target_address_error_count == len(test_address_list) - 1

    correct_address_list = ['sqlite:///test.db']
    for address in correct_address_list:
        index = address[Constant.MIN_ADDRESS_LENGTH - 1:].rfind('/')
        try:
            if not os.access(address[Constant.MIN_ADDRESS_LENGTH - 1:index] if index != -1 else './', os.W_OK):
                raise ValueError(
                    ErrorMsg.NO_ACCESS.get_msg('. No access path: %s' % address[Constant.MIN_ADDRESS_LENGTH - 1:index]))
        except ValueError as v:
            assert v.__str__() == '. No access path: %s' % address[Constant.MIN_ADDRESS_LENGTH - 1:index]
