import flask
import pytest
from flask_sqlalchemy import SQLAlchemy


@pytest.fixture
def app(request):
    app = flask.Flask(request.module.__name__)
    app.testing = True
    app.config['SQLALCHEMY_BINDS']['flask_state_sqlite'] = 'sqlite:///'