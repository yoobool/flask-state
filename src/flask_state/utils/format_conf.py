import os
import platform

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
            ErrorMsg.DATA_TYPE_ERROR.get_msg('. The target type is {}, not {}'.format(int.__name__, type(secs).__name__)))
    if secs < Constant.MIN_SECONDS:
        logger.warning(WarningMsg.TIME_SMALL.get_msg())
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
            ErrorMsg.DATA_TYPE_ERROR.get_msg('.The target type is {}, not {}'.format(str.__name__, type(address).__name__)))
    if len(address) < Constant.MIN_ADDRESS_LENGTH or address[:Constant.MIN_ADDRESS_LENGTH - 1] != DB_URL_HEADER:
        raise ValueError(ErrorMsg.ERROR_ADDRESS.get_msg('.Error sqlite url: %s' % address))
    if platform.system() == Constant.WINDOWS_SYSTEM:
        index = max(address[Constant.MIN_ADDRESS_LENGTH - 1:].rfind('\\'), address[Constant.MIN_ADDRESS_LENGTH - 1:].rfind('/'))
    else:
        index = address[Constant.MIN_ADDRESS_LENGTH - 1:].rfind('/')
    db_path = address[Constant.MIN_ADDRESS_LENGTH - 1:][:index] if index != -1 else './'
    if not os.access(db_path, os.W_OK):
        raise ValueError(ErrorMsg.NO_ACCESS.get_msg('. No access path: %s' % address))
    return address
