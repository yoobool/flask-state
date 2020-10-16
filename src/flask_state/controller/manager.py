import json
import logging
import time
from concurrent.futures import ThreadPoolExecutor
from flask import request, current_app
from .response_methods import make_response_content
from ..models import model_init_app
from ..services import redis_conn, flask_state_conf
from ..services.host_status import query_flask_state_host, record_flask_state_host
from ..exceptions import ErrorResponse, CustomError
from ..exceptions.error_code import MsgCode
from ..utils.auth import auth_user, auth_method
from ..utils.file_lock import Lock
from ..conf.config import HttpMethod


def init_app(app):
    """
    Plugin entry
    :param app: Flask app

    """
    app.add_url_rule('/v0/state/hoststatus', endpoint='state_host_status', view_func=query_flask_state,
                     methods=[HttpMethod.POST.value])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    if not app.config.get('SQLALCHEMY_BINDS') or not app.config['SQLALCHEMY_BINDS'].get('flask_state_sqlite'):
        raise CustomError('You must to set up SQLALCHEMY_BINDS and bind flask_state_sqlite')
    if app.config.get('REDIS_CONF') and app.config.get('REDIS_CONF', {}).get('REDIS_STATUS'):
        redis_state = app.config['REDIS_CONF']
        redis_conf = {'REDIS_HOST': redis_state.get('REDIS_HOST'), 'REDIS_PORT': redis_state.get('REDIS_PORT'),
                      'REDIS_PASSWORD': redis_state.get('REDIS_PASSWORD')}
        redis_conn.set_redis(redis_conf)
    model_init_app(app)
    app.lock = Lock.get_file_lock()

    # Timing recorder
    def record_timer():
        with app.app_context():
            try:
                current_app.lock.acquire()
                while True:
                    pre_time = time.time()
                    record_flask_state_host()
                    now_time = time.time()
                    time.sleep(flask_state_conf.SECS - (now_time - pre_time))
            except Exception as e:
                current_app.lock.release()
                raise e

    ThreadPoolExecutor(max_workers=1).submit(record_timer)


@auth_user
@auth_method
def query_flask_state():
    """
    Query the local state and redis status
    :return: flask response
    """
    try:
        b2d = json.loads(request.data)
        if not isinstance(b2d, dict):
            return make_response_content(MsgCode.JSON_FORMAT_ERROR)
        time_quantum = b2d.get('timeQuantum')
        return make_response_content(resp=query_flask_state_host(time_quantum))
    except Exception as e:
        logging.exception(e)
        return make_response_content(ErrorResponse(MsgCode.UNKNOWN_ERROR))
