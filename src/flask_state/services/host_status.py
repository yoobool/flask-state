import os
import platform
import sys

import psutil

from . import redis_conn
from ..conf.config import Constant, DAYS_SCOPE
from ..dao.host_status import create_host_status, retrieve_host_status, retrieve_host_status_yesterday
from ..exceptions import FlaskStateResponse, SuccessResponse, ErrorResponse
from ..exceptions.error_code import MsgCode
from ..utils.date import get_current_ms, get_current_s
from ..utils.format_conf import get_file_inf
from ..utils.logger import logger

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
                logger.warning(t, extra=get_file_inf(sys._getframe()))
        create_host_status(result_conf)
    except Exception as e:
        logger.exception(e, extra=get_file_inf(sys._getframe()))
        raise e


def query_flask_state_host(days) -> FlaskStateResponse:
    """
    Query the local status and redis status of [1,3,7,30] days
    :param days: the query days
    :return: flask response
    """
    try:
        if days not in DAYS_SCOPE:
            return ErrorResponse(MsgCode.OVERSTEP_DAYS_SCOPE)
        result = retrieve_host_status(days)
        arr = []
        for status in result:
            load_avg = (status.load_avg or '').split(',')
            host_dict = row2dict(status)
            host_dict.update(load_avg=load_avg)
            arr.append(host_dict)
        data = {"currentStatistic": arr[0] if arr else {}, "items": []}
        fields = ["cpu", "memory", "load_avg", "disk_usage"]
        for item in arr:
            statistics_item = [int(item['ts'] / SECONDS_TO_MILLISECOND_MULTIPLE)]
            for field in fields:
                statistics_item.append(item[field])
            data["items"].append(statistics_item)
        return SuccessResponse(msg='Search success', data=data)
    except Exception as e:
        logger.exception(e, extra=get_file_inf(sys._getframe()))
        return ErrorResponse(MsgCode.UNKNOWN_ERROR)


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
