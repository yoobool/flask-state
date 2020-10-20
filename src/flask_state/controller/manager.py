import sys
import time
from concurrent.futures import ThreadPoolExecutor

from flask import request, current_app

from .response_methods import make_response_content
from ..conf.config import HttpMethod, Constant
from ..exceptions import ErrorResponse
from ..exceptions.error_code import MsgCode
from ..exceptions.log_msg import ErrorMsg
from ..models import model_init_app
from ..services import redis_conn
from ..services.host_status import query_flask_state_host, record_flask_state_host
from ..utils.auth import auth_user, auth_method
from ..utils.file_lock import Lock
from ..utils.format_conf import format_address, get_file_inf, format_sec
from ..utils.logger import logger, DefaultLogger

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

    ThreadPoolExecutor(max_workers=1).submit(record_timer, app, interval)


def init_redis(app):
    if app.config.get('REDIS_CONF', {}).get('REDIS_STATUS'):
        redis_state = app.config['REDIS_CONF']
        redis_conf = {'REDIS_HOST': redis_state.get('REDIS_HOST'), 'REDIS_PORT': redis_state.get('REDIS_PORT'),
                      'REDIS_PASSWORD': redis_state.get('REDIS_PASSWORD')}
        redis_conn.set_redis(redis_conf)


def init_db(app):
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    if not app.config.get('SQLALCHEMY_BINDS', {}).get('flask_state_sqlite'):
        raise KeyError(ErrorMsg.LACK_SQLITE.get_msg())
    app.config['SQLALCHEMY_BINDS']['flask_state_sqlite'] = format_address(
        app.config['SQLALCHEMY_BINDS'].get('flask_state_sqlite'))


def record_timer(app, interval):
    app.lock_flask_state = Lock.get_file_lock()
    with app.app_context():
        try:
            current_app.lock_flask_state.acquire()
            in_time = time.time()
            target_time = int(int((time.time()) / ONE_MINUTE_SECONDS + 1) * ONE_MINUTE_SECONDS)
            time.sleep(ONE_MINUTE_SECONDS - in_time % ONE_MINUTE_SECONDS)
            while True:
                record_flask_state_host(interval)
                target_time += interval
                now_time = time.time()
                time.sleep(target_time - now_time)
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
                '.The target type is %s, not %s' % (dict.__name__, type(b2d).__name__),
                extra=get_file_inf(sys._getframe()))
            return make_response_content(ErrorResponse(MsgCode.JSON_FORMAT_ERROR))
        time_quantum = b2d.get('timeQuantum')
        return make_response_content(resp=query_flask_state_host(time_quantum))
    except Exception as e:
        logger.exception(e, extra=get_file_inf(sys._getframe()))
        return make_response_content(ErrorResponse(MsgCode.UNKNOWN_ERROR), http_status=500)
