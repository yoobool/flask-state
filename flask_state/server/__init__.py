import redis
from enum import unique, Enum
from ..utils.format_conf import format_sec, format_address

# Query time range
DAYS_SCOPE = {'1': 1, '3': 3, '7': 7, '30': 30}


class DefaultConf:
    def __init__(self):
        # Set the ID of the binding element in HTML, or select the suspension ball binding
        # The default value is(False, 'console_machine_status')
        self.ID_NAME = ('console_machine_status', True)

        # Set plugin language
        self.LANGUAGE = 'English'

        # Enter the database name, address and conf directory or superior directory, the default is 0
        # If the project has a console_host database, it is not created
        # The default value is('console_host', 0)
        self.ADDRESS = 'sqlite:///console_host'

        # Set the interval to record the local state, with a minimum interval of 10 seconds
        # The default value is 60
        self.SECS = 60

    def set_id_name(self, element, ball=True):
        self.ID_NAME = format_id_name(element, ball)

    def set_language(self, language):
        self.LANGUAGE = format_language(language)

    def set_address(self, address):
        self.ADDRESS = format_address(address)

    def set_secs(self, secs):
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
