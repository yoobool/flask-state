import math
import os
import platform
from collections import namedtuple
from datetime import datetime, timezone

import psutil

from ..conf.config import Config
from ..dao.host_status import (
    create_host_io,
    create_host_status,
    delete_thirty_days_io_status,
    delete_thirty_days_status,
    retrieve_host_status,
    retrieve_host_status_yesterday,
    retrieve_io_status,
    retrieve_latest_host_status,
    retrieve_latest_io_status,
)
from ..exceptions import FlaskStateError, FlaskStateResponse, SuccessResponse
from ..exceptions.error_code import MsgCode
from ..exceptions.log_msg import ErrorMsg
from ..utils.constants import HTTPStatus, NumericConstants, TimeConstants
from ..utils.date import get_current_ms, get_current_s, get_formatted_timestamp
from ..utils.logger import logger
from . import redis_conn


def record_flask_state_host(interval, target_time):
    """
    Record local status and monitor redis status

    """
    if get_current_s() - target_time > Config.ABANDON_THRESHOLD:
        format_date = get_formatted_timestamp(target_time)
        logger.error(ErrorMsg.RUN_TIME_ERROR.get_msg(". Target time is {}".format(format_date)))
        return

    try:
        result_conf = {}
        host_status = query_host_info()
        result_conf.update(host_status)
        redis_status = query_redis_info()
        result_conf.update(redis_status)

        create_host_status(result_conf)
        now_time = get_current_s()
        new_day_utc = (
            datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0, tzinfo=timezone.utc).timestamp()
        )
        if now_time <= new_day_utc + interval:
            delete_thirty_days_status()

    except Exception as e:
        logger.exception(e)


def query_host_info():
    """
    Collect host status
    :return host status dict
    :rtype: dict
    """
    cpu = psutil.cpu_percent(interval=Config.CPU_PERCENT_INTERVAL)
    memory = psutil.virtual_memory().percent
    if platform.system() == "Windows":
        load_avg = Config.DEFAULT_WINDOWS_LOAD_AVG
    else:
        load_avg = ",".join([str(float("%.2f" % x)) for x in os.getloadavg()])
    disk_usage = psutil.disk_usage("/").percent
    boot_ts = psutil.boot_time()
    result = {
        "ts": get_current_ms(),
        "cpu": cpu,
        "memory": memory,
        "load_avg": load_avg,
        "disk_usage": disk_usage,
        "boot_seconds": int(get_current_s() - boot_ts),
    }
    return result


def query_redis_info():
    """
    Collect redis status
    :return: redis status dict
    :rtype: dict
    """
    result = {}
    redis_handler = redis_conn.get_redis()
    if redis_handler:
        try:
            redis_info = redis_handler.info()
            used_memory = redis_info.get("used_memory")
            used_memory_rss = redis_info.get("used_memory_rss")
            connected_clients = redis_info.get("connected_clients")
            uptime_in_seconds = redis_info.get("uptime_in_seconds")
            mem_fragmentation_ratio = redis_info.get("mem_fragmentation_ratio")
            keyspace_hits = redis_info.get("keyspace_hits")
            keyspace_misses = redis_info.get("keyspace_misses")
            hits_ratio = (
                float("%.2f" % (keyspace_hits * NumericConstants.PERCENTAGE / (keyspace_hits + keyspace_misses)))
                if (keyspace_hits + keyspace_misses) != 0
                else Config.DEFAULT_HITS_RATIO
            )
            delta_hits_ratio = hits_ratio
            yesterday_current_statistic = retrieve_host_status_yesterday()
            if yesterday_current_statistic:
                yesterday_keyspace_hits = yesterday_current_statistic.keyspace_hits
                yesterday_keyspace_misses = yesterday_current_statistic.keyspace_misses
                if yesterday_keyspace_hits is not None and yesterday_keyspace_misses is not None:
                    be_divided_num = (
                        keyspace_hits + keyspace_misses - (yesterday_keyspace_hits + yesterday_keyspace_misses)
                    )
                    delta_hits_ratio = (
                        float(
                            "%.2f"
                            % ((keyspace_hits - yesterday_keyspace_hits) * NumericConstants.PERCENTAGE / be_divided_num)
                        )
                        if be_divided_num != 0
                        else Config.DEFAULT_DELTA_HITS_RATIO
                    )
            result.update(
                used_memory=used_memory,
                used_memory_rss=used_memory_rss,
                connected_clients=connected_clients,
                uptime_in_seconds=uptime_in_seconds,
                mem_fragmentation_ratio=mem_fragmentation_ratio,
                keyspace_hits=keyspace_hits,
                keyspace_misses=keyspace_misses,
                hits_ratio=hits_ratio,
                delta_hits_ratio=delta_hits_ratio,
            )
        except Exception as t:
            logger.exception(t)
    return result


def record_flask_state_io_host(interval, target_time):
    """
    Record local status and monitor redis status

    """
    if get_current_s() - target_time > Config.ABANDON_IO_THRESHOLD:
        format_date = get_formatted_timestamp(target_time)
        logger.error(ErrorMsg.RUN_TIME_ERROR.get_msg(". Target time is {}".format(format_date)))
        return

    try:
        result_conf = {}
        host_io_status = query_host_io_info()
        result_conf.update(host_io_status)

        create_host_io(result_conf)
        now_time = get_current_s()
        new_day_utc = (
            datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0, tzinfo=timezone.utc).timestamp()
        )
        if now_time <= new_day_utc + interval:
            delete_thirty_days_io_status()

    except Exception as e:
        logger.exception(e)


def query_host_io_info():
    """
    Collect host io status
    :return host status dict
    :rtype: dict
    """
    try:
        net_sent = psutil.net_io_counters().bytes_sent
        net_recv = psutil.net_io_counters().bytes_recv
        disk_read = psutil.disk_io_counters().read_bytes
        disk_write = psutil.disk_io_counters().write_bytes
    except:
        net_sent = 0
        net_recv = 0
        disk_read = 0
        disk_write = 0
    result = {
        "net_sent": net_sent,
        "net_recv": net_recv,
        "disk_read": disk_read,
        "disk_write": disk_write,
        "ts": get_current_ms(),
    }
    return result


def query_flask_state_host(days) -> FlaskStateResponse:
    """
    Query the local status and redis status of [1,3,7,30] days
    :param days: the query days
    :return: flask response
    """
    if str(days).isnumeric():
        days = int(days)
    else:
        raise FlaskStateError(**MsgCode.PARAMETER_ERROR.value, status_code=HTTPStatus.BAD_REQUEST)

    if days not in TimeConstants.DAYS_SCOPE:
        raise FlaskStateError(**MsgCode.OVERSTEP_DAYS_SCOPE.value, status_code=HTTPStatus.BAD_REQUEST)
    try:
        io_info = {}
        now_ts = get_current_ms()
        now_io = query_host_io_info()
        latest_io = retrieve_latest_io_status()
        if latest_io and math.ceil((now_ts - latest_io.get("ts")) / 1000) <= 60:
            interval = math.ceil((now_ts - latest_io.get("ts")) / 1000)
            io_info.update(
                {
                    "net_sent": (now_io.get("net_sent") - latest_io.get("net_sent")) / interval,
                    "net_recv": (now_io.get("net_recv") - latest_io.get("net_recv")) / interval,
                    "disk_read": (now_io.get("disk_read") - latest_io.get("disk_read")) / interval,
                    "disk_write": (now_io.get("disk_write") - latest_io.get("disk_write")) / interval,
                }
            )
        else:
            io_info.update(
                {
                    "net_sent": 0,
                    "net_recv": 0,
                    "disk_read": 0,
                    "disk_write": 0,
                }
            )
        current_status = query_host_info()
        current_status.update(query_redis_info())
        current_status.update(io_info)
        current_status["load_avg"] = (current_status.get("load_avg") or "").split(",")
    except:
        current_status = retrieve_latest_host_status()
        current_status["load_avg"] = (current_status.get("load_avg") or "").split(",")
    result = retrieve_host_status(days)
    result = control_result_counts(result)
    io_result = retrieve_io_status(days)
    io_result = control_io_counts(io_result)
    arr = []
    io_arr = []
    for status in result:
        arr.append(
            [
                int(status.ts / TimeConstants.SECONDS_TO_MILLISECOND_MULTIPLE),
                status.cpu,
                status.memory,
                status.load_avg.split(","),
            ]
        )
    for io_state in io_result:
        io_arr.append(
            [
                int(io_state.ts / TimeConstants.SECONDS_TO_MILLISECOND_MULTIPLE),
                io_state.net_recv,
                io_state.net_sent,
            ]
        )
    data = {"currentStatistic": current_status, "items": arr, "io": io_arr}
    return SuccessResponse(msg="Search success", data=data)


def control_result_counts(result) -> list:
    """
    Control the search results to the specified number
    :param result: db query result
    :return: result after treatment
    """
    result_length = len(result)
    if result_length > Config.MAX_RETURN_RECORDS:
        refine_result = []
        interval = round(result_length / Config.MAX_RETURN_RECORDS, 2)
        index = 0
        while index <= result_length - 1 and len(refine_result) < Config.MAX_RETURN_RECORDS:
            refine_result.append(result[int(index)])
            index += interval
        result = refine_result
    return result


def control_io_counts(result) -> list:
    result_length = len(result)
    io_tuple = namedtuple("io", "net_recv, net_sent, ts")
    if result_length > Config.MAX_RETURN_RECORDS:
        refine_result = []
        interval = round(result_length / Config.MAX_RETURN_RECORDS, 2)
        index = 0
        while index < result_length - 1 and len(refine_result) < Config.MAX_RETURN_RECORDS:
            new_tmp = result[int(index)]
            old_tmp = result[int(index + 1)]
            now_item = io_tuple(new_tmp.net_recv - old_tmp.net_recv, new_tmp.net_sent - old_tmp.net_sent, new_tmp.ts)
            refine_result.append(now_item)
            index += interval
        result = refine_result
    else:
        refine_result = []
        for index in range(result_length - 1):
            now_item = io_tuple(
                result[index].net_recv - result[index + 1].net_recv,
                result[index].net_sent - result[index + 1].net_sent,
                result[index].ts,
            )
            refine_result.append(now_item)
        result = refine_result
    return result


def row2dict(field):
    """
    Model class to dictionary class
    :param field: database query results
    :return: database query results dictionary
    """
    d = {}
    for column in field.__table__.columns:
        if column.name not in ("create_time", "update_time"):
            d[column.name] = getattr(field, column.name)
    return d
