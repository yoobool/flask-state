import os
import platform

from ..conf.config import DEFAULT_SECONDS, DEFAULT_BIND_SQLITE, DEFAULT_DB_URL
from ..exceptions.error_msg import ErrorMsg, WarningMsg
from ..utils.logger import logger

MIN_SECONDS = 10  # Optional minimum number of seconds

MIN_ADDRESS_LENGTH = 11  # minimum number of address length

DB_URL_HEADER = 'sqlite:///'  # Database URL specification header

WINDOWS_SYSTEM = 'Windows'  # Windows system


def format_sec(secs):
    """
    Format incoming time
    :param secs: initial time
    :return: format time
    """
    if not isinstance(secs, int) or secs < MIN_SECONDS:
        return DEFAULT_SECONDS
    else:
        return secs


def format_address(address):
    """
    Format incoming database address
    :param address: initial database address
    :return: format database address
    """
    if not isinstance(address, str):
        logger.warning(WarningMsg.DATA_TYPE_ERROR.get_msg())
        address = str(address)
    if len(address) < MIN_ADDRESS_LENGTH or address[:MIN_ADDRESS_LENGTH - 1] != DB_URL_HEADER:
        logger.exception(ErrorMsg.ERROR_ADDRESS.get_msg())
        raise ValueError(DEFAULT_BIND_SQLITE)
    if platform.system() == WINDOWS_SYSTEM:
        index = max(address.rfind('\\'), address.rfind('/'))
    else:
        index = address.rfind('/')
    if os.access(address[10:index] if index != -1 else './', os.W_OK):
        path = address
    else:
        logger.warning(WarningMsg.NO_ACCESS.get_msg())
        path = DEFAULT_DB_URL
    return path
