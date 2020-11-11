import os
import sched
import threading
import time

from flask import current_app, request

from ..conf.config import Constant, HttpMethod
from ..exceptions import ErrorResponse
from ..exceptions.error_code import MsgCode
from ..exceptions.log_msg import ErrorMsg, InfoMsg
from ..models import model_init_app
from ..services import redis_conn
from ..services.host_status import query_flask_state_host, record_flask_state_host
from ..utils.auth import auth_method, auth_user
from ..utils.file_lock import Lock
from ..utils.format_conf import format_address, format_sec
from ..utils.logger import DefaultLogger, logger
from .response_methods import make_response_content

ONE_MINUTE_SECONDS = 60


def init_app(app, interval=Constant.DEFAULT_SECONDS, log_instance=None):
    """
    Plugin entry
    :param app: Flask app
    :param interval: record interval
    :param log_instance: custom logger object
    """
    logger.set(log_instance or DefaultLogger().get())
    app.add_url_rule('/v0/state/hoststatus', endpoint='state_host_status', view_func=query_flask_state,
                     methods=[HttpMethod.POST.value])
    init_db(app)
    init_redis(app)
    model_init_app(app)

    # Timing recorder
    interval = format_sec(interval)
    t = threading.Thread(target=record_timer, args=(app, interval,))
    t.setDaemon(True)
    t.start()


def init_redis(app):
    redis_state = app.config.get('REDIS_CONF', {})

    if not redis_state.get('REDIS_STATUS'):
        return

    redis_conf_keys = ['REDIS_HOST', 'REDIS_PORT', 'REDIS_PASSWORD']
    redis_conf = {key: value for key, value in redis_state.items() if key in redis_conf_keys}

    redis_conn.set_redis(redis_conf)


def init_db(app):
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    if not app.config.get('SQLALCHEMY_BINDS', {}).get(Constant.DEFAULT_BIND_SQLITE):
        raise KeyError(ErrorMsg.LACK_SQLITE.get_msg())
    app.config['SQLALCHEMY_BINDS'][Constant.DEFAULT_BIND_SQLITE] = format_address(
        app.config['SQLALCHEMY_BINDS'].get(Constant.DEFAULT_BIND_SQLITE))


def record_timer(app, interval):
    app.lock_flask_state = Lock.get_file_lock()
    with app.app_context():
        try:
            current_app.lock_flask_state.acquire()
            logger.info(InfoMsg.ACQUIRED_LOCK.get_msg('. process ID: %d' % os.getpid()))

            s = sched.scheduler(time.time, time.sleep)
            in_time = time.time()
            target_time = int(int((time.time()) / ONE_MINUTE_SECONDS + 1) * ONE_MINUTE_SECONDS)
            time.sleep(ONE_MINUTE_SECONDS - in_time % ONE_MINUTE_SECONDS)
            record_flask_state_host(interval)
            while True:
                target_time += interval
                now_time = time.time()
                s.enter(target_time - now_time, 1, record_flask_state_host, (interval,))
                s.run()
        except BlockingIOError:
            pass
        except Exception as e:
            current_app.lock_flask_state.release()
            raise e


@auth_user
@auth_method
def query_flask_state():
    """
    Query the local state and redis status
    :return: flask response
    """
    try:
        b2d = request.json
        if not isinstance(b2d, dict):
            logger.warning(ErrorMsg.DATA_TYPE_ERROR).get_msg(
                '.The target type is {}, not {}'.format(dict.__name__, type(b2d).__name__))
            return make_response_content(ErrorResponse(MsgCode.JSON_FORMAT_ERROR))
        time_quantum = b2d.get('timeQuantum')
        return make_response_content(resp=query_flask_state_host(time_quantum))
    except Exception as e:
        logger.exception(e)
        return make_response_content(ErrorResponse(MsgCode.UNKNOWN_ERROR), http_status=500)
