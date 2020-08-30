import psutil
import os
import platform
import logging
import redis
from . import RedisObj, MsgCode, DAYS_SCOPE
from .response_methods import make_response_content
from ..dao.host_status import create_host_status, retrieve_host_status, retrieve_host_status_yesterday, \
    retrieve_one_host_status
from ..utils.date import get_current_ms, get_current_s


def record_console_host():
    """
    Record local status and monitor redis status

    """
    try:
        cpu = psutil.cpu_percent(interval=0)
        memory = psutil.virtual_memory().percent
        if platform.system() == 'Windows':
            load_avg = '0, 0, 0'
        else:
            load_avg = ','.join([str(float('%.2f' % x)) for x in os.getloadavg()])
        disk_usage = psutil.disk_usage('/').percent
        boot_ts = psutil.boot_time()
        result_obj = {'ts': get_current_ms(), 'cpu': cpu, 'memory': memory, 'load_avg': load_avg,
                      'disk_usage': disk_usage,
                      'boot_seconds': int(get_current_s() - boot_ts)}
        console_handler = RedisObj.get_redis()
        if console_handler:
            try:
                redis_info = console_handler.info()
                used_memory = redis_info.get('used_memory')
                used_memory_rss = redis_info.get('used_memory_rss')
                connected_clients = redis_info.get('connected_clients')
                uptime_in_seconds = redis_info.get('uptime_in_seconds')
                mem_fragmentation_ratio = redis_info.get('mem_fragmentation_ratio')
                keyspace_hits = redis_info.get('keyspace_hits')
                keyspace_misses = redis_info.get('keyspace_misses')
                hits_ratio = float('%.2f' % (keyspace_hits * 100 / (keyspace_hits + keyspace_misses))) if \
                    (keyspace_hits + keyspace_misses) != 0 else 100
                delta_hits_ratio = hits_ratio
                yesterday_current_statistic = retrieve_host_status_yesterday()
                if yesterday_current_statistic:
                    yesterday_keyspace_hits = yesterday_current_statistic.keyspace_hits
                    yesterday_keyspace_misses = yesterday_current_statistic.keyspace_misses
                    if yesterday_keyspace_hits is not None and yesterday_keyspace_misses is not None:
                        be_divided_num = keyspace_hits + keyspace_misses - (
                                yesterday_keyspace_hits + yesterday_keyspace_misses)
                        delta_hits_ratio = float(
                            '%.2f' % ((keyspace_hits - yesterday_keyspace_hits) * 100 / be_divided_num)) \
                            if be_divided_num != 0 else 100
                result_obj.update(used_memory=used_memory,
                                  used_memory_rss=used_memory_rss,
                                  connected_clients=connected_clients,
                                  uptime_in_seconds=uptime_in_seconds,
                                  mem_fragmentation_ratio=mem_fragmentation_ratio,
                                  keyspace_hits=keyspace_hits,
                                  keyspace_misses=keyspace_misses,
                                  hits_ratio=hits_ratio,
                                  delta_hits_ratio=delta_hits_ratio)
            except Exception as t:
                logging.error(t)
        create_host_status(result_obj)
    except Exception as e:
        logging.error(e)
        raise e


def query_console_host(days='1') -> dict:
    """
    Query the local status and redis status of [1,3,7,30] days
    :param days: the query days
    :return: flask response
    """
    try:
        if days not in DAYS_SCOPE:
            return make_response_content(MsgCode.OVERSTEP_DAYS_SCOPE)
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
            statistics_item = [int(item['ts'] / 1000)]
            for field in fields:
                statistics_item.append(item[field])
            data["items"].append(statistics_item)
        return make_response_content(msg='Search success', data=data)
    except Exception as e:
        logging.error(e)
        return make_response_content(MsgCode.UNKNOWN_ERROR)


def query_one_min_record():
    """
    Check whether there are records inserted within one minute
    :return: True or False
    """
    try:
        data = retrieve_one_host_status()
        if not data:
            return True
        if (get_current_ms() - data.ts) < 60000:
            return False
        return True
    except Exception as e:
        logging.error(e)
        return make_response_content(MsgCode.UNKNOWN_ERROR)


def row2dict(obj):
    """
    Model class to dictionary class
    :param obj: database query results
    :return: database query results dictionary
    """
    d = {}
    for column in obj.__table__.columns:
        if column.name not in ('create_time', 'update_time'):
            d[column.name] = getattr(obj, column.name)
    return d
