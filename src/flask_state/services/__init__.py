from ..conf.config import Config
from ..exceptions.log_msg import WarningMsg
from ..utils.logger import logger


# Create redis object
class RedisConn:
    def __init__(self):
        self.redis = None

    def set_redis(self, redis_conf):
        try:
            import redis

            self.redis = redis.Redis(
                host=redis_conf.get("REDIS_HOST"),
                port=redis_conf.get("REDIS_PORT"),
                password=redis_conf.get("REDIS_PASSWORD"),
                socket_connect_timeout=Config.REDIS_CONNECT_TIMEOUT,
                socket_timeout=Config.REDIS_TIMEOUT,
            )
        except ImportError:
            logger.warning(WarningMsg.LACK_REDIS.get_msg())
            self.redis = None

    def get_redis(self):
        return self.redis


redis_conn = RedisConn()
