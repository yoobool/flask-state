import os
import platform
import warnings

from ..conf.config import MAX_TIME_SCALE, Constant, TimeScale
from ..exceptions.log_msg import ErrorMsg, WarningMsg
from ..utils.logger import logger

DB_URL_HEADER = "sqlite:///"  # Database URL specification header
TIME_LENGTH = 1
TIME_RANGE_LENGTH = 2
LAST_TIME_SCALE_LENGTH = 1


def format_sec(secs) -> int:
    warnings.warn("format_sec will be deprecated", DeprecationWarning)
    """
    Format incoming time
    :param secs: initial time
    :return: format time
    :rtype: int
    """
    if not isinstance(secs, int):
        raise TypeError(
            ErrorMsg.DATA_TYPE_ERROR.get_msg(
                ". The target type is {}, not {}".format(int.__name__, type(secs).__name__)
            )
        )
    if secs < Constant.MIN_SECONDS:
        logger.warning(WarningMsg.TIME_SMALL.get_msg())
        return Constant.DEFAULT_SECONDS
    return secs


def format_address(address) -> str:
    """
    Format incoming database address
    :param address: initial database address
    :return: format database address
    :rtype: str
    """
    if not isinstance(address, str):
        raise TypeError(
            ErrorMsg.DATA_TYPE_ERROR.get_msg(
                ".The target type is {}, not {}".format(str.__name__, type(address).__name__)
            )
        )
    if len(address) < Constant.MIN_ADDRESS_LENGTH or address[: Constant.MIN_ADDRESS_LENGTH - 1] != DB_URL_HEADER:
        raise ValueError(ErrorMsg.ERROR_ADDRESS.get_msg(".Error sqlite url: %s" % address))
    if platform.system() == Constant.WINDOWS_SYSTEM:
        index = max(
            address[Constant.MIN_ADDRESS_LENGTH - 1 :].rfind("\\"),
            address[Constant.MIN_ADDRESS_LENGTH - 1 :].rfind("/"),
        )
    else:
        index = address[Constant.MIN_ADDRESS_LENGTH - 1 :].rfind("/")
    db_path = address[Constant.MIN_ADDRESS_LENGTH - 1 :][:index] if index != -1 else "./"
    if not os.access(db_path, os.W_OK):
        raise ValueError(ErrorMsg.NO_ACCESS.get_msg(". No access path: %s" % address))
    return address


def format_cron(scope_tuple) -> list:
    """
    Format the input time range
    :param scope_tuple: a tuple of time scale name and initial range. E.g. ('HOUR', '10, 22-23')
    :return: a list of time_scale
    :rtype: list
    """
    scale_name, scope = scope_tuple
    now_time_scale = Constant.MIN_DAY_SCALE if scale_name == TimeScale.DAY.value else Constant.MIN_TIME_SCALE
    max_time_scale = MAX_TIME_SCALE.get(scale_name, 0)
    if not isinstance(scope, str):
        raise TypeError(
            ErrorMsg.DATA_TYPE_ERROR.get_msg(
                ".The target type is {}, not {}".format(str.__name__, type(scope).__name__)
            )
        )
    get_separation = scope.split(",")
    get_range = list()
    for separation in get_separation:
        range_tmp = separation.split("-")
        range_tmp_len = len(range_tmp)
        try:
            if range_tmp_len == TIME_LENGTH:
                time_scale = int(range_tmp[0])
                if now_time_scale < time_scale < max_time_scale:
                    now_time_scale = time_scale
                else:
                    raise ValueError
                get_range.append(time_scale)
            elif range_tmp_len == TIME_RANGE_LENGTH:
                for time_scale in range(int(range_tmp[0]), int(range_tmp[1]) + LAST_TIME_SCALE_LENGTH):
                    if now_time_scale < time_scale < max_time_scale:
                        now_time_scale = time_scale
                    else:
                        raise ValueError
                    get_range.append(time_scale)
            else:
                raise ValueError
        except ValueError:
            raise ValueError(ErrorMsg.ERROR_CRON.get_msg(".Wrong parameter is {}: {}".format(scale_name, scope)))
    return get_range


def format_cron_sec(cron_sec) -> int:
    """
    Format the input second range
    :param cron_sec: initial second value
    :return: int(cron_sec)
    :rtype: int
    """
    if not isinstance(cron_sec, str):
        raise TypeError(
            ErrorMsg.DATA_TYPE_ERROR.get_msg(
                ".The target type is {}, not {}".format(str.__name__, type(cron_sec).__name__)
            )
        )
    scale_name = TimeScale.SECOND.value
    min_second_scale = Constant.MIN_TIME_SCALE
    max_second_scale = MAX_TIME_SCALE.get(scale_name)
    try:
        time_scale = int(cron_sec)
        if not min_second_scale < time_scale < max_second_scale:
            raise ValueError
    except ValueError:
        raise ValueError(ErrorMsg.ERROR_CRON.get_msg(".Wrong parameter is {}: {}".format(scale_name, cron_sec)))
    return time_scale
