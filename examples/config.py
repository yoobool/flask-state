import os
import sys

from flask import Flask

from flask_state import DEFAULT_BIND_SQLITE, init_app

# SQLite URI compatible
WIN = sys.platform.startswith("win")
if WIN:
    prefix = "sqlite:///"
else:
    prefix = "sqlite:////"


def setting_app():
    app = Flask(__name__)

    # Redis conf
    app.config["REDIS_CONF"] = {
        "REDIS_STATUS": True,
        "REDIS_HOST": "127.0.0.1",
        "REDIS_PORT": 16379,
        "REDIS_PASSWORD": "password",
    }
    path_ = os.getcwd() + "/flask_state_host.db"
    app.config["SQLALCHEMY_BINDS"] = {DEFAULT_BIND_SQLITE: prefix + path_}

    # log_instance = logging.getLogger(__name__)
    # use init_app initial configuration
    init_app(app, interval=60)
    return app
