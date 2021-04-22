import json
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
from ..utils.file_lock import db_lock
from ..utils.logger import logger
from . import redis_conn


def record_flask_state_host(interval, target_time):
    """
    Record local status and monitor redis status

    """
    if get_current_s() - target_time > Config.ABANDON_THRESHOLD:
        format_date = get_formatted_timestamp(target_time)
        logger.error(
            ErrorMsg.RUN_TIME_ERROR.get_msg(
                ". Target time is {}".format(format_date)
            )
        )
        return

    try:
        result_conf = {}
        host_status = query_host_info()
        del host_status["users"]
        result_conf.update(host_status)
        redis_status = query_redis_info()
        result_conf.update(redis_status)

        db_lock.acquire()
        create_host_status(result_conf)
        now_time = get_current_s()
        new_day_utc = (
            datetime.utcnow()
            .replace(
                hour=0, minute=0, second=0, microsecond=0, tzinfo=timezone.utc
            )
            .timestamp()
        )
        if now_time <= new_day_utc + interval:
            delete_thirty_days_status()
    except Exception as e:
        logger.exception(str(e))
    finally:
        db_lock.release()


def query_host_info():
    """
    Collect host status
    :return host status dict
    :rtype: dict
    """
    cpus = psutil.cpu_percent(interval=Config.CPU_PERCENT_INTERVAL, percpu=True)
    core_number = len(cpus)
    cpu = round(sum(cpus) / core_number, 1)
    memory = psutil.virtual_memory().percent
    if platform.system() == "Windows":
        load_avg = Config.DEFAULT_WINDOWS_LOAD_AVG
    else:
        load_avg = ",".join([str(float("%.2f" % x)) for x in os.getloadavg()])
    disk_usage = psutil.disk_usage("/").percent
    boot_ts = psutil.boot_time()
    users = [
        {"n": user.name, "t": user.terminal} for user in psutil.users() or []
    ]
    result = {
        "ts": get_current_ms(),
        "cpu": cpu,
        "cpus": str(cpus).replace(" ", ""),
        "memory": memory,
        "load_avg": load_avg,
        "disk_usage": disk_usage,
        "boot_seconds": int(get_current_s() - boot_ts),
        "users": users,
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
                float(
                    "%.2f"
                    % (
                        keyspace_hits
                        * NumericConstants.PERCENTAGE
                        / (keyspace_hits + keyspace_misses)
                    )
                )
                if (keyspace_hits + keyspace_misses) != 0
                else Config.DEFAULT_HITS_RATIO
            )
            delta_hits_ratio = hits_ratio
            yesterday_current_statistic = retrieve_host_status_yesterday()
            if yesterday_current_statistic:
                yesterday_keyspace_hits = (
                    yesterday_current_statistic.keyspace_hits
                )
                yesterday_keyspace_misses = (
                    yesterday_current_statistic.keyspace_misses
                )
                if (
                    yesterday_keyspace_hits is not None
                    and yesterday_keyspace_misses is not None
                ):
                    be_divided_num = (
                        keyspace_hits
                        + keyspace_misses
                        - (yesterday_keyspace_hits + yesterday_keyspace_misses)
                    )
                    delta_hits_ratio = (
                        float(
                            "%.2f"
                            % (
                                (keyspace_hits - yesterday_keyspace_hits)
                                * NumericConstants.PERCENTAGE
                                / be_divided_num
                            )
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
            logger.exception(str(t))
    return result


def record_flask_state_io_host(interval, target_time):
    """
    Record local status and monitor redis status

    """
    if get_current_s() - target_time > Config.ABANDON_IO_THRESHOLD:
        format_date = get_formatted_timestamp(target_time)
        logger.error(
            ErrorMsg.RUN_TIME_ERROR.get_msg(
                ". Target time is {}".format(format_date)
            )
        )
        return

    try:
        result_conf = {}
        host_io_status = query_host_io_info()
        result_conf.update(host_io_status)

        db_lock.acquire()
        create_host_io(result_conf)
        now_time = get_current_s()
        new_day_utc = (
            datetime.utcnow()
            .replace(
                hour=0, minute=0, second=0, microsecond=0, tzinfo=timezone.utc
            )
            .timestamp()
        )
        if now_time <= new_day_utc + interval:
            delete_thirty_days_io_status()
    except Exception as e:
        logger.exception(str(e))
    finally:
        db_lock.release()


def query_host_io_info():
    """
    Collect host io status
    :return host status dict
    :rtype: dict
    """
    net_io = psutil.net_io_counters()
    disk_io = psutil.disk_io_counters()
    net_sent = net_io.bytes_sent if net_io else 0
    net_recv = net_io.bytes_recv if net_io else 0
    disk_read = disk_io.read_bytes if disk_io else 0
    disk_write = disk_io.write_bytes if disk_io else 0
    packets_sent = net_io.packets_sent if net_io else 0
    packets_recv = net_io.packets_recv if net_io else 0
    read_count = disk_io.read_count if disk_io else 0
    write_count = disk_io.write_count if disk_io else 0
    result = {
        "net_sent": net_sent,
        "net_recv": net_recv,
        "disk_read": disk_read,
        "disk_write": disk_write,
        "packets_sent": packets_sent,
        "packets_recv": packets_recv,
        "read_count": read_count,
        "write_count": write_count,
        "ts": get_current_ms(),
    }
    return result


def get_io_pers():
    """
    Get current network io data
    :rtype: dict
    """
    now_ts = get_current_ms()
    now_io = query_host_io_info()
    io_data = {}
    latest_io = retrieve_latest_io_status()
    if latest_io and math.ceil((now_ts - latest_io.get("ts")) / 1000) <= 60:
        interval = math.ceil((now_ts - latest_io.get("ts")) / 1000)
        io_data.update(
            {
                "net_sent": (
                    max(now_io.get("net_sent") - latest_io.get("net_sent"), 0)
                )
                / interval,
                "net_recv": (
                    max(now_io.get("net_recv") - latest_io.get("net_recv"), 0)
                )
                / interval,
                "packets_sent": max(
                    now_io.get("packets_sent") - latest_io.get("packets_sent"),
                    0,
                ),
                "packets_recv": max(
                    now_io.get("packets_recv") - latest_io.get("packets_recv"),
                    0,
                ),
                "disk_read": (
                    max(now_io.get("disk_read") - latest_io.get("disk_read"), 0)
                )
                / interval,
                "disk_write": (
                    max(
                        now_io.get("disk_write") - latest_io.get("disk_write"),
                        0,
                    )
                )
                / interval,
                "read_count": max(
                    now_io.get("read_count") - latest_io.get("read_count"), 0
                ),
                "write_count": max(
                    now_io.get("write_count") - latest_io.get("write_count"), 0
                ),
            }
        )
    else:
        io_data.update(
            {
                "net_sent": 0,
                "net_recv": 0,
                "packets_sent": 0,
                "packets_recv": 0,
                "disk_read": 0,
                "disk_write": 0,
                "read_count": 0,
                "write_count": 0,
            }
        )
    return io_data


def query_flask_state_host(days) -> FlaskStateResponse:
    """
    Query the local status and redis status of [1,3,7,30] days
    :param days: the query days
    :return: flask response
    """
    if str(days).isnumeric():
        days = int(days)
    else:
        raise FlaskStateError(
            **MsgCode.PARAMETER_ERROR.value, status_code=HTTPStatus.BAD_REQUEST
        )

    if days not in TimeConstants.DAYS_SCOPE:
        raise FlaskStateError(
            **MsgCode.OVERSTEP_DAYS_SCOPE.value,
            status_code=HTTPStatus.BAD_REQUEST
        )
    try:
        current_status = query_host_info()
        current_status.update(query_redis_info())
        current_status.update(get_io_pers())
    except Exception:
        current_status = retrieve_latest_host_status()
    current_status["load_avg"] = (current_status.get("load_avg") or "").split(
        ","
    )
    cpu_count = psutil.cpu_count()
    current_status["cpu_count"] = cpu_count

    host_result = control_result_counts(retrieve_host_status(days))
    host_arr = {
        "ts": [],
        "cpu": [],
        "loadavg": [],
        "loadavg5": [],
        "loadavg15": [],
        "memory": [],
    }
    for i in range(cpu_count):
        host_arr["cpu{num}".format(num=i)] = []
    for status in host_result:
        host_arr["ts"].append(
            int(status.ts / TimeConstants.SECONDS_TO_MILLISECOND_MULTIPLE)
        )
        loadavg_arr = status.load_avg.split(",")
        host_arr["loadavg"].append(loadavg_arr[0])
        host_arr["loadavg5"].append(loadavg_arr[1])
        host_arr["loadavg15"].append(loadavg_arr[2])
        host_arr["memory"].append(status.memory)
        cpus = json.loads(status.cpus)
        for i in range(-1, cpu_count):
            if i == -1:
                host_arr["cpu"].append(status.cpu)
            else:
                host_arr["cpu{num}".format(num=i)].append(
                    cpus[i] if len(cpus) > i else 0
                )

    io_result = control_io_counts(retrieve_io_status())
    io_result.reverse()
    io_arr = {
        "ts": [],
        "net_recv": [],
        "net_sent": [],
        "disk_read": [],
        "disk_write": [],
        "packets_recv": [],
        "packets_sent": [],
        "read_count": [],
        "write_count": [],
    }
    for io_state in io_result:
        io_arr["ts"].append(
            int(io_state.ts / TimeConstants.SECONDS_TO_MILLISECOND_MULTIPLE)
        )
        io_arr["net_recv"].append(io_state.net_recv)
        io_arr["net_sent"].append(io_state.net_sent)
        io_arr["disk_read"].append(io_state.disk_read)
        io_arr["disk_write"].append(io_state.disk_write)
        io_arr["packets_recv"].append(io_state.packets_recv)
        io_arr["packets_sent"].append(io_state.packets_sent)
        io_arr["read_count"].append(io_state.read_count)
        io_arr["write_count"].append(io_state.write_count)
    data = {"currentStatistic": current_status, "host": host_arr, "io": io_arr}
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
        while (
            index <= result_length - 1
            and len(refine_result) < Config.MAX_RETURN_RECORDS
        ):
            refine_result.append(result[int(index)])
            index += interval
        result = refine_result
    return result


def control_io_counts(result) -> list:
    """
    Control the io search results to the specified number
    :param result: db query result
    :return: result after treatment
    """
    result_length = len(result)
    io_tuple = namedtuple(
        "io",
        "net_recv, net_sent, disk_read, disk_write, packets_recv, packets_sent, read_count, write_count, ts",
    )
    if result_length > Config.MAX_RETURN_RECORDS:
        refine_result = []
        interval = round(result_length / Config.MAX_RETURN_RECORDS, 2)
        index = 0
        while (
            index < result_length - 1
            and len(refine_result) < Config.MAX_RETURN_RECORDS
        ):
            if (
                result[int(index)].ts - result[int(index + 1)].ts
                > TimeConstants.FIF_SECOND_TO_MILLSECOND
            ):
                index += interval
                continue
            new_tmp = result[int(index)]
            old_tmp = result[int(index + 1)]
            now_item = io_tuple(
                max(new_tmp.net_recv - old_tmp.net_recv, 0),
                max(new_tmp.net_sent - old_tmp.net_sent, 0),
                max(new_tmp.disk_read - old_tmp.disk_read, 0),
                max(new_tmp.disk_write - old_tmp.disk_write, 0),
                max(new_tmp.packets_recv - old_tmp.packets_recv, 0),
                max(new_tmp.packets_sent - old_tmp.packets_sent, 0),
                max(new_tmp.read_count - old_tmp.read_count, 0),
                max(new_tmp.write_count - old_tmp.write_count, 0),
                new_tmp.ts,
            )
            refine_result.append(now_item)
            index += interval
        result = refine_result
    else:
        refine_result = []
        for index in range(result_length - 1):
            if (
                result[index].ts - result[index + 1].ts
                > TimeConstants.FIF_SECOND_TO_MILLSECOND
            ):
                continue
            now_item = io_tuple(
                result[index].net_recv - result[index + 1].net_recv,
                result[index].net_sent - result[index + 1].net_sent,
                result[index].disk_read - result[index + 1].disk_read,
                result[index].disk_write - result[index + 1].disk_write,
                result[index].packets_recv - result[index + 1].packets_recv,
                result[index].packets_sent - result[index + 1].packets_sent,
                result[index].read_count - result[index + 1].read_count,
                result[index].write_count - result[index + 1].write_count,
                result[index].ts,
            )
            refine_result.append(now_item)
        result = refine_result
    return result
