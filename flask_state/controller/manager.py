import json
import logging
import time
from concurrent.futures import ThreadPoolExecutor

from flask import request, current_app

from ..models import model_init_app
from ..server import RedisObj, default_conf_obj
from ..server.host_status import query_console_host, MsgCode, record_console_host
from ..server.response_methods import make_response_content
from ..utils.auth import auth_user, auth_method
from ..utils.file_lock import Lock


def init_app(app):
    """
    Plugin entry
    :param app: Flask app

    """
    app.add_url_rule('/v0/state/hoststatus', endpoint='state_host_status', view_func=query_console_status,
                     methods=['POST'])
    if not app.config.get('SQLALCHEMY_BINDS') or not app.config['SQLALCHEMY_BINDS'].get('flask_state_sqlite'):
        app.config['SQLALCHEMY_BINDS'] = app.config.get('SQLALCHEMY_BINDS') or {}
        app.config['SQLALCHEMY_BINDS']['flask_state_sqlite'] = default_conf_obj.ADDRESS
    if app.config.get('REDIS_CONF') and app.config['REDIS_CONF'].get('REDIS_STATUS'):
        redis_state = app.config['REDIS_CONF']
        redis_obj = {'REDIS_HOST': redis_state.get('REDIS_HOST'), 'REDIS_PORT': redis_state.get('REDIS_PORT'),
                     'REDIS_PASSWORD': redis_state.get('REDIS_PASSWORD')}
        RedisObj.set_redis(redis_obj)
    model_init_app(app)
    app.lock = Lock.get_file_lock()

    # Timing recorder
    def record_timer():
        with app.app_context():
            try:
                current_app.lock.acquire()
                while True:
                    record_console_host()
                    time.sleep(default_conf_obj.SECS - 0.02)
            except Exception as e:
                current_app.lock.release()
                raise e

    ThreadPoolExecutor(max_workers=1).submit(record_timer)


@auth_user
@auth_method
def query_console_status():
    """
    Query the local state and redis status
    :return: flask response
    """
    try:
        b2d = json.loads(request.data)
        if not isinstance(b2d, dict):
            return make_response_content(MsgCode.JSON_FORMAT_ERROR)
        time_quantum = b2d.get('timeQuantum')
        return query_console_host(time_quantum)
    except Exception as e:
        print(e)
        logging.error(e)
        return make_response_content(MsgCode.UNKNOWN_ERROR)
