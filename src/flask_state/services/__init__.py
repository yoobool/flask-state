import redis

from ..conf.config import Constant


# Create redis object
class RedisConn:
    def __init__(self):
        self.redis = None

    def set_redis(self, redis_conf):
        self.redis = redis.Redis(host=redis_conf.get('REDIS_HOST'), port=redis_conf.get('REDIS_PORT'),
                                 password=redis_conf.get('REDIS_PASSWORD'), socket_connect_timeout=Constant.REDIS_TIMEOUT)

    def get_redis(self) -> redis.Redis:
        return self.redis


redis_conn = RedisConn()
