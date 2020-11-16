from flask import Flask

from src.flask_state import DEFAULT_BIND_SQLITE, init_app


def setting_app():
    app = Flask(__name__)

    # Redis conf
    app.config["REDIS_CONF"] = {
        "REDIS_STATUS": True,
        "REDIS_HOST": "192.168.0.2",
        "REDIS_PORT": 16379,
        "REDIS_PASSWORD": "fish09",
    }

    import os

    path_ = os.getcwd() + "/flask_state_host.db"
    app.config["SQLALCHEMY_BINDS"] = {DEFAULT_BIND_SQLITE: "sqlite:///" + path_}

    # log_instance = logging.getLogger(__name__)
    # use init_app initial configuration
    init_app(app, 60)
    return app
