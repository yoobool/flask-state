import os
import platform
import sys

from ..conf.config import Constant
from ..exceptions.log_msg import ErrorMsg, WarningMsg
from ..utils.logger import logger

DB_URL_HEADER = 'sqlite:///'  # Database URL specification header


def format_sec(secs) -> int:
    """
    Format incoming time
    :param secs: initial time
    :return: format time
    """
    if not isinstance(secs, int):
        raise TypeError(
            ErrorMsg.DATA_TYPE_ERROR.get_msg('.The target type is %s, not %s' % (int.__name__, type(secs).__name__)))
    if secs < Constant.MIN_SECONDS:
        logger.warning(WarningMsg.TIME_SMALL.get_msg(), extra=get_file_inf(sys._getframe()))
        return Constant.DEFAULT_SECONDS
    return secs


def format_address(address) -> str:
    """
    Format incoming database address
    :param address: initial database address
    :return: format database address
    """
    if not isinstance(address, str):
        raise TypeError(
            ErrorMsg.DATA_TYPE_ERROR.get_msg('.The target type is %s, not %s' % (str.__name__, type(address).__name__)))
    if len(address) < Constant.MIN_ADDRESS_LENGTH or address[:Constant.MIN_ADDRESS_LENGTH - 1] != DB_URL_HEADER:
        raise ValueError(ErrorMsg.ERROR_ADDRESS.get_msg())
    if platform.system() == Constant.WINDOWS_SYSTEM:
        index = max(address.rfind('\\'), address.rfind('/'))
    else:
        index = address.rfind('/')
    if not os.access(address[10:index] if index != -1 else './', os.W_OK):
        raise ValueError(ErrorMsg.NO_ACCESS.get_msg())
    return address


def get_file_inf(get_frame) -> dict:
    """
    Get the current file name, function name, line number
    :param get_frame: sys.frame class
    :return: dict of file name, function name, line number
    """
    return {
        'handlerFileName': 'flask_state.' + get_frame.f_code.co_filename.split('flask_state/')[-1].replace('/', '.')[
                                            :-3], 'handlerFuncName': get_frame.f_code.co_name,
        'handlerLine': get_frame.f_lineno}
