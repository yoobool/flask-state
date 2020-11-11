import os
import platform
from datetime import datetime, timezone

import psutil

from ..conf.config import DAYS_SCOPE, Constant
from ..dao.host_status import (
    create_host_status,
    delete_thirty_days_status,
    retrieve_host_status,
    retrieve_host_status_yesterday,
    retrieve_latest_host_status,
)
from ..exceptions import ErrorResponse, FlaskStateResponse, SuccessResponse
from ..exceptions.error_code import MsgCode
from ..utils.date import get_current_ms, get_current_s
from ..utils.logger import logger
from . import redis_conn

SECONDS_TO_MILLISECOND_MULTIPLE = 1000  # Second to millisecond multiple
DEFAULT_HITS_RATIO = 100  # Default hits ratio value
DEFAULT_DELTA_HITS_RATIO = 100  # Default 24h hits ratio value
DEFAULT_WINDOWS_LOAD_AVG = '0, 0, 0'  # Windows system cannot calculate load AVG
PERCENTAGE = 100  # Percentage calculation


def record_flask_state_host(interval):
    """
    Record local status and monitor redis status

    """
    try:
        cpu = psutil.cpu_percent(interval=Constant.CPU_PERCENT_INTERVAL)
        memory = psutil.virtual_memory().percent
        if platform.system() == 'Windows':
            load_avg = DEFAULT_WINDOWS_LOAD_AVG
        else:
            load_avg = ','.join([str(float('%.2f' % x)) for x in os.getloadavg()])
        disk_usage = psutil.disk_usage('/').percent
        boot_ts = psutil.boot_time()
        result_conf = {'ts': get_current_ms(), 'cpu': cpu, 'memory': memory, 'load_avg': load_avg,
                       'disk_usage': disk_usage,
                       'boot_seconds': int(get_current_s() - boot_ts)}
        redis_handler = redis_conn.get_redis()
        if redis_handler:
            try:
                redis_info = redis_handler.info()
                used_memory = redis_info.get('used_memory')
                used_memory_rss = redis_info.get('used_memory_rss')
                connected_clients = redis_info.get('connected_clients')
                uptime_in_seconds = redis_info.get('uptime_in_seconds')
                mem_fragmentation_ratio = redis_info.get('mem_fragmentation_ratio')
                keyspace_hits = redis_info.get('keyspace_hits')
                keyspace_misses = redis_info.get('keyspace_misses')
                hits_ratio = float('%.2f' % (keyspace_hits * PERCENTAGE / (keyspace_hits + keyspace_misses))) if \
                    (keyspace_hits + keyspace_misses) != 0 else DEFAULT_HITS_RATIO
                delta_hits_ratio = hits_ratio
                yesterday_current_statistic = retrieve_host_status_yesterday()
                if yesterday_current_statistic:
                    yesterday_keyspace_hits = yesterday_current_statistic.keyspace_hits
                    yesterday_keyspace_misses = yesterday_current_statistic.keyspace_misses
                    if yesterday_keyspace_hits is not None and yesterday_keyspace_misses is not None:
                        be_divided_num = keyspace_hits + keyspace_misses - (
                                yesterday_keyspace_hits + yesterday_keyspace_misses)
                        delta_hits_ratio = float(
                            '%.2f' % ((keyspace_hits - yesterday_keyspace_hits) * PERCENTAGE / be_divided_num)) \
                            if be_divided_num != 0 else DEFAULT_DELTA_HITS_RATIO
                result_conf.update(used_memory=used_memory,
                                   used_memory_rss=used_memory_rss,
                                   connected_clients=connected_clients,
                                   uptime_in_seconds=uptime_in_seconds,
                                   mem_fragmentation_ratio=mem_fragmentation_ratio,
                                   keyspace_hits=keyspace_hits,
                                   keyspace_misses=keyspace_misses,
                                   hits_ratio=hits_ratio,
                                   delta_hits_ratio=delta_hits_ratio)
            except Exception as t:
                logger.warning(t)
        create_host_status(result_conf)
        now_time = get_current_s()
        new_day_utc = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0,
                                                tzinfo=timezone.utc).timestamp()
        if now_time <= new_day_utc + interval:
            delete_thirty_days_status()

    except Exception as e:
        logger.exception(e)


def query_flask_state_host(days) -> FlaskStateResponse:
    """
    Query the local status and redis status of [1,3,7,30] days
    :param days: the query days
    :return: flask response
    """
    try:
        try:
            if not isinstance(days, int):
                days = int(days)
        except Exception as t:
            raise t
        if days not in DAYS_SCOPE:
            return ErrorResponse(MsgCode.OVERSTEP_DAYS_SCOPE)
        current_status = retrieve_latest_host_status()
        current_status['load_avg'] = (current_status.get('load_avg') or '').split(',')
        result = retrieve_host_status(days)
        result = control_result_counts(result)
        arr = []
        for status in result:
            arr.append([int(status.ts / SECONDS_TO_MILLISECOND_MULTIPLE), status.cpu, status.memory,
                        status.load_avg.split(','), status.disk_usage])
        data = {"currentStatistic": current_status, "items": arr}
        return SuccessResponse(msg='Search success', data=data)
    except Exception as e:
        logger.exception(e)
        return ErrorResponse(MsgCode.UNKNOWN_ERROR)


def control_result_counts(result) -> list:
    """
    Control the search results to the specified number
    :param result: db query result
    :return: result after treatment
    """
    result_length = len(result)
    if result_length > Constant.MAX_RETURN_RECORDS:
        refine_result = list()
        interval = round(result_length / Constant.MAX_RETURN_RECORDS, 2)
        index = 0
        while index <= result_length - 1 and len(refine_result) < Constant.MAX_RETURN_RECORDS:
            refine_result.append(result[int(index)])
            index += interval
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
        if column.name not in ('create_time', 'update_time'):
            d[column.name] = getattr(field, column.name)
    return d
