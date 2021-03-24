import os
import sched
import threading
import time

from flask import current_app, request

from ..conf.config import Config
from ..controller.interceptors import json_required
from ..exceptions import ErrorResponse, FlaskStateError
from ..exceptions.error_code import MsgCode
from ..exceptions.log_msg import ErrorMsg, InfoMsg
from ..models import model_init_app
from ..services import redis_conn
from ..services.host_status import (
    query_flask_state_host,
    record_flask_state_host,
    record_flask_state_io_host,
)
from ..utils.auth import auth_method, auth_user
from ..utils.constants import HttpMethod, HTTPStatus
from ..utils.file_lock import Lock
from ..utils.logger import DefaultLogger, logger
from .response_methods import make_response_content


@auth_user
@auth_method
@json_required
def query_flask_state():
    """
    Query the local state and redis status
    :return: flask response
    """
    try:
        b2d = request.json
        time_quantum = b2d.get("timeQuantum")
        return make_response_content(resp=query_flask_state_host(time_quantum))
    except FlaskStateError as e:
        logger.warning(e)
        return make_response_content(e, http_status=e.status_code)
    except Exception as e:
        logger.exception(str(e))
        error_response = ErrorResponse(MsgCode.UNKNOWN_ERROR)
        http_status = HTTPStatus.INTERNAL_SERVER_ERROR
        return make_response_content(error_response, http_status=http_status)


def init_url_rules(app):
    """
    Initialize the flask-state route
    :param app: flask app
    """
    app.add_url_rule(
        "/v0/state/hoststatus",
        endpoint="state_host_status",
        view_func=query_flask_state,
        methods=[HttpMethod.POST.value],
    )


def init_redis(app):
    """
    Initialize redis connection
    :param app: flask app
    """
    state = app.config.get("REDIS_CONF", {})
    if state.get("REDIS_STATUS"):
        keys = ["REDIS_HOST", "REDIS_PORT", "REDIS_PASSWORD"]
        conf = {key: value for key, value in state.items() if key in keys}
        redis_conn.set_redis(conf)


def init_db(app):
    """
    Determine whether the flask-state database is bound correctly
    :param app: flask app
    """
    sqlalchemy_binds = app.config["SQLALCHEMY_BINDS"]
    if Config.DEFAULT_BIND_SQLITE not in sqlalchemy_binds:
        raise KeyError(ErrorMsg.LACK_SQLITE.get_msg())


def record_timer(app, function, interval, lock_group, lock_key, priority=1):
    with app.app_context():
        app.locks[lock_group][lock_key] = Lock.get_file_lock(lock_key)
        try:
            current_app.locks[lock_group][lock_key].acquire()
            if lock_key == "host":
                logger.info(InfoMsg.ACQUIRED_LOCK.get_msg(". process ID: {id}".format(id=os.getpid())))

            scheduler = sched.scheduler(time.time, time.sleep)
            event = {
                "action": function,
                "priority": priority,
                "kwargs": {
                    "interval": interval,
                    "target_time": int(int((time.time()) / 60 + 1) * 60),
                },
            }
            time.sleep(event["kwargs"]["target_time"] - time.time())
            function(**event["kwargs"])
            while True:
                target_time = event["kwargs"]["target_time"] + interval
                event["kwargs"]["target_time"] = target_time
                event["delay"] = target_time - time.time()
                scheduler.enter(**event)
                scheduler.run()
        except BlockingIOError:
            # The process that failed to obtain the lock resource exits directly
            pass
        except Exception as e:
            current_app.locks[lock_group][lock_key].release()
            raise e


def init_recorder_threads(app, interval):
    lock_group = "record_flask_state"
    app.locks = {lock_group: {}}
    target_kwargs = {"app": app, "lock_group": lock_group}

    threads = {}
    threads["host"] = threading.Thread(
        target=record_timer,
        kwargs={"function": record_flask_state_host, "interval": interval, "lock_key": "host", **target_kwargs},
    )
    threads["io"] = threading.Thread(
        target=record_timer,
        kwargs={"function": record_flask_state_io_host, "interval": 10, "lock_key": "io", **target_kwargs},
    )

    return threads


def init_app(app, interval=60, log_instance=None):
    """
    Plugin entry
    :param app: Flask app
    :param interval:
    :param log_instance: custom logger object
    """
    logger.set(log_instance or DefaultLogger())

    if not isinstance(interval, int):
        raise TypeError(
            ErrorMsg.DATA_TYPE_ERROR.get_msg(
                ".The target type is {}, not {}".format(int.__name__, type(interval).__name__)
            )
        )

    init_url_rules(app)
    init_db(app)
    init_redis(app)
    model_init_app(app)

    recorder_threads = init_recorder_threads(app, interval)
    for thread in recorder_threads.values():
        thread.setDaemon(True)
        thread.start()
