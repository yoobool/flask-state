import flask
import pytest

from src.flask_state import DEFAULT_BIND_SQLITE


@pytest.fixture
def app():
    app = flask.Flask("test_app")
    app.testing = True
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
    app.config["SQLALCHEMY_BINDS"] = {DEFAULT_BIND_SQLITE: "sqlite:///test.db"}
    app.config["REDIS_CONF"] = {
        "REDIS_STATE": True,
        "REDIS_HOST": "192.168.0.2",
        "REDIS_PORT": 16379,
        "REDIS_PASSWORD": "fish09",
    }
    return app
