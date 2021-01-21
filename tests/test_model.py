import os
import warnings

import psutil

from src.flask_state.conf import config
from src.flask_state.dao import host_status
from src.flask_state.models import model_init_app
from src.flask_state.utils import date


def test_model(app):
    """
    Test whether the model field is correct
    :param app: test Flask(__name__)
    """
    model_init_app(app)

    # insert data
    cpu = psutil.cpu_percent(interval=config.Config.CPU_PERCENT_INTERVAL)
    memory = psutil.virtual_memory().percent
    try:
        load_avg = ",".join([str(float("%.2f" % x)) for x in os.getloadavg()])
    except AttributeError:
        load_avg = "0, 0, 0"
    disk_usage = psutil.disk_usage("/").percent
    boot_ts = psutil.boot_time()
    result_conf = {
        "ts": date.get_current_ms(),
        "cpu": cpu,
        "memory": memory,
        "load_avg": load_avg,
        "disk_usage": disk_usage,
        "boot_seconds": int(date.get_current_s() - boot_ts),
    }
    with app.app_context():
        host_status.create_host_status(result_conf)

    # query data
    with app.app_context():
        result = host_status.retrieve_host_status(1)[0]
        assert result is not None

    # clear data
    with app.app_context():
        result = host_status.FlaskStateHost.query.delete(synchronize_session=False)
        if result:
            host_status.db.session.commit()


def test_clear_expire_data(app):
    """
    Test deleting expired data
    :param app: test Flask(__name__)
    """
    model_init_app(app)
    expire_data_length = 5
    thirty_day = 30

    # insert expire data
    for i in range(expire_data_length):
        cpu = psutil.cpu_percent(interval=config.Config.CPU_PERCENT_INTERVAL)
        memory = psutil.virtual_memory().percent
        try:
            load_avg = ",".join([str(float("%.2f" % x)) for x in os.getloadavg()])
        except AttributeError:
            load_avg = "0, 0, 0"
        disk_usage = psutil.disk_usage("/").percent
        boot_ts = psutil.boot_time()
        result_conf = {
            "ts": 0,
            "cpu": cpu,
            "memory": memory,
            "load_avg": load_avg,
            "disk_usage": disk_usage,
            "boot_seconds": int(date.get_current_s() - boot_ts),
        }
        with app.app_context():
            host_status.create_host_status(result_conf)

    # clear expire data
    with app.app_context():
        target_time = date.get_current_ms() - date.get_query_ms(thirty_day)
        result = host_status.FlaskStateHost.query.filter(host_status.FlaskStateHost.ts < target_time).delete(
            synchronize_session=False
        )
        assert result == expire_data_length
        if result:
            host_status.db.session.commit()
