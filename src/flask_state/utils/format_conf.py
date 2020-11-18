import os
import platform

from ..exceptions.log_msg import ErrorMsg
from .constants import CronConstants, DBAddressConstants, OperatingSystem, TimeScale


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
    if (
        len(address) < DBAddressConstants.MIN_ADDRESS_LENGTH
        or address[: DBAddressConstants.MIN_ADDRESS_LENGTH - 1] != DBAddressConstants.DB_URL_HEADER
    ):
        raise ValueError(ErrorMsg.ERROR_ADDRESS.get_msg(".Error sqlite url: %s" % address))
    if platform.system() == OperatingSystem.WINDOWS_SYSTEM:
        index = max(
            address[DBAddressConstants.MIN_ADDRESS_LENGTH - 1 :].rfind("\\"),
            address[DBAddressConstants.MIN_ADDRESS_LENGTH - 1 :].rfind("/"),
        )
    else:
        index = address[DBAddressConstants.MIN_ADDRESS_LENGTH - 1 :].rfind("/")
    db_path = address[DBAddressConstants.MIN_ADDRESS_LENGTH - 1 :][:index] if index != -1 else "./"
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
    not_allow_time_scale = (
        CronConstants.NOT_ALLOW_DAY_SCALE if scale_name == TimeScale.DAY.value else CronConstants.NOT_ALLOW_TIME_SCALE
    )
    max_time_scale = CronConstants.MAX_TIME_SCALE.get(scale_name, 0)
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
            if range_tmp_len == CronConstants.NOT_RANGE_LENGTH:
                time_scale = int(range_tmp[0])
                if not_allow_time_scale < time_scale < max_time_scale:
                    not_allow_time_scale = time_scale
                else:
                    raise ValueError
                get_range.append(time_scale)
            elif range_tmp_len == CronConstants.IS_RANGE_LENGTH:
                for time_scale in range(int(range_tmp[0]), int(range_tmp[1]) + CronConstants.SELECT_LAST_TIME_SCALE):
                    if not_allow_time_scale < time_scale < max_time_scale:
                        not_allow_time_scale = time_scale
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
    not_allow_second_scale = CronConstants.NOT_ALLOW_TIME_SCALE
    max_second_scale = CronConstants.MAX_TIME_SCALE.get(scale_name)
    try:
        time_scale = int(cron_sec)
        if not not_allow_second_scale < time_scale < max_second_scale:
            raise ValueError
    except ValueError:
        raise ValueError(ErrorMsg.ERROR_CRON.get_msg(".Wrong parameter is {}: {}".format(scale_name, cron_sec)))
    return time_scale
