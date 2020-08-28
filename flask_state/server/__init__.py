import redis
from enum import unique, Enum
from ..utils.format_conf import format_id_name, format_sec, format_address, format_language

# Query time range
DAYS_SCOPE = {'1': 1, '3': 3, '7': 7, '30': 30}

# Display language
LANGUAGE = {
    'Chinese': {'language': '0', 'host_status': '本机状态', 'cpu': '中央处理器', 'memory': '内存', 'disk_usage': '磁盘使用率',
                'load_avg': 'LoadAvg',
                'boot_seconds': '启动时长', 'redis_status': 'Redis状态', 'used_memory': '分配总内存',
                'used_memory_rss': '使用内存', 'mem_fragmentation_ratio': '内存碎片率', 'hits_ratio': '缓存命中率',
                'delta_hits_ratio': '24小时缓存命中率', 'uptime_in_seconds': '启动时长',
                'connected_clients': '当前连接数', 'days': '天', 'hours': '小时', 'minutes': '分钟', 'seconds': '秒',
                'today': '今天'},
    'English': {'language': '1', 'host_status': 'host_status', 'cpu': 'cpu', 'memory': 'memory',
                'disk_usage': 'disk_usage',
                'load_avg': 'LoadAvg',
                'boot_seconds': 'boot_seconds', 'redis_status': 'redis_status', 'used_memory': 'used_memory',
                'used_memory_rss': 'used_memory_rss', 'mem_fragmentation_ratio': 'mem_fragmentation_ratio',
                'hits_ratio': 'hits_ratio',
                'delta_hits_ratio': 'delta_hits_ratio', 'uptime_in_seconds': 'uptime_in_seconds',
                'connected_clients': 'connected_clients', 'days': 'days', 'hours': 'hours', 'minutes': 'minutes',
                'seconds': 'seconds', 'today': 'today'}
}


class DefaultConf:
    def __init__(self):
        # Set the ID of the binding element in HTML, or select the suspension ball binding
        # The default value is(False, 'console_machine_status')
        self.ID_NAME = (True, 'console_machine_status')

        # Set plugin language
        self.LANGUAGE = 'Chinese'

        # Enter the database name, address and conf directory or superior directory, the default is 0
        # If the project has a console_host database, it is not created
        # The default value is('console_host', 0)
        self.ADDRESS = 'sqlite:///console_host'

        # Set the interval to record the local state, with a minimum interval of 10 seconds
        # The default value is 60
        self.SECS = 60

    def set_id_name(self, element=None, ball=True):
        self.ID_NAME = format_id_name(element, ball)

    def set_language(self, language=None):
        self.LANGUAGE = format_language(language)

    def set_address(self, address=None, catalogue=0):
        self.ADDRESS = format_address(address, catalogue)

    def set_secs(self, secs=None):
        self.SECS = format_sec(secs)


default_conf_obj = DefaultConf()


# Create redis object
class RedisConn(object):
    def __init__(self):
        self.redis = None

    def set_redis(self, redis_conf):
        self.redis = redis.Redis(host=redis_conf.get('REDIS_HOST'), port=redis_conf.get('REDIS_PORT'),
                                 password=redis_conf.get('REDIS_PASSWORD'), socket_connect_timeout=1)

    def get_redis(self) -> redis.Redis:
        return self.redis


RedisObj = RedisConn()


# Enumeration function
@unique
class ResponseMsg(Enum):
    def get_code(self):
        return self.value.get('code')

    def get_msg(self):
        return self.value.get('msg')


# Return behavior msg and status code
class MsgCode(ResponseMsg):
    # success
    SUCCESS = {'msg': 'SUCCESS', 'code': '200'}

    # fail
    OVERSTEP_DAYS_SCOPE = {'msg': 'Exceeding the allowed query time range', 'code': '10001'}
    REQUEST_METHOD_ERROR = {'msg': 'The request method cannot be get', 'code': '10002'}
    NOT_SUPPORT_LANGUAGE = {'msg': 'Language not supported', 'code': '10003'}
    ERROR_TYPE = {'msg': 'Wrong parameter type', 'code': '10004'}
    JSON_FORMAT_ERROR = {'msg': 'JSON format is required', 'code': '10005'}
    AUTH_FAIL = {'msg': 'Validation failed', 'code': '10006'}
    UNKNOWN_ERROR = {'msg': 'Unknown error', 'code': '10007'}
