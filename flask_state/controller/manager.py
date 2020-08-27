import json
import logging
from flask import request, current_app
from concurrent.futures import ThreadPoolExecutor
from ..models import model_init_app
from ..utils.file_lock import Lock
from ..utils.format_conf import format_sec, format_address
from ..conf.config import default_conf_obj
from ..server import RedisObj
from ..server.host_status import query_console_host, MsgCode, record_console_host
from ..server.language import return_language
from ..server.bind_id import send_id
from ..server.response_methods import make_response_content


def init_app(app):
    """
    Plugin entry
    :param app: Flask app

    """
    default_conf_obj.set_id_name((False, 'console_machine_status'))
    app.add_url_rule('/v0/state/hoststatus', endpoint='state_host_status', view_func=query_console_status, methods=['POST'])
    app.add_url_rule('/v0/state/bindid', endpoint='state_bind_id', view_func=bind_id2element, methods=['POST'])
    app.add_url_rule('/v0/state/language', endpoint='state_language', view_func=get_language, methods=['POST'])
    if not app.config.get('SQLALCHEMY_BINDS') or not app.config['SQLALCHEMY_BINDS'].get('flask_state_sqlite'):
        app.config['SQLALCHEMY_BINDS'] = app.config.get('SQLALCHEMY_BINDS') or {}
        app.config['SQLALCHEMY_BINDS']['flask_state_sqlite'] = format_address(default_conf_obj.ADDRESS)
    if app.config.get('REDIS_CONF') and app.config['REDIS_CONF'].get('REDIS_REDIS_STATUS'):
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
                    time.sleep(format_sec(default_conf_obj.SECS) - 0.02)
            except Exception as e:
                current_app.lock.release()
                raise e

    ThreadPoolExecutor(max_workers=1).submit(record_timer)

def query_console_status():
    """
    Query the local state and redis status
    :return: flask response
    """
    try:
        if request.method == 'POST':
            time_quantum = json.loads(request.data)['timeQuantum']
            if not time_quantum:
                time_quantum = '1'
            return query_console_host(time_quantum)
        else:
            return make_response_content(MsgCode.REQUEST_METHOD_ERROR)
    except Exception as e:
        raise e


def bind_id2element():
    """
    Bind triggers to observe the element ID of the native window
    :return: flask response
    """
    try:
        if request.method == 'POST':
            if not isinstance(default_conf_obj.ID_NAME, tuple):
                return make_response_content(MsgCode.ERROR_TYPE)
            return send_id(default_conf_obj.ID_NAME)
    except Exception as e:
        raise e


def get_language():
    """
    Select presentation language
    :return: flask response
    """
    try:
        if request.method == 'POST':
            language = default_conf_obj.LANGUAGE
            if not language:
                language = 'Chinese'
            return return_language(language)
        else:
            return make_response_content(MsgCode.REQUEST_METHOD_ERROR)
    except Exception as e:
        logging.ERROR(e)
        raise e
