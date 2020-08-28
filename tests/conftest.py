import flask
import pytest
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from sqlalchemy.sql import text


@pytest.fixture
def app(request):
    app = flask.Flask('test_app')
    app.testing = True
    app.config['SQLALCHEMY_BINDS'] = {'flask_state_sqlite': 'sqlite:///console_host'}
    app.config['REDIS_CONF'] = {'REDIS_STATE': True, 'REDIS_HOST': '192.168.0.2', 'REDIS_PORT': 16379,
                                'REDIS_PASSWORD': 'fish09'}
    return app


@pytest.fixture
def db(app):
    return SQLAlchemy(app)


@pytest.fixture
def host(db):
    class ConsoleHost(db.Model):
        __bind_key__ = 'flask_state_sqlite'
        __tablename__ = "console_host"
        id = db.Column(db.Integer, primary_key=True, autoincrement=True)
        create_time = db.Column(db.DateTime, server_default=func.now())
        update_time = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())

        #console
        cpu = db.Column(db.Float, server_default=text("0"))
        memory = db.Column(db.Float, server_default=text("0"))
        load_avg = db.Column(db.String(32), server_default="")
        disk_usage = db.Column(db.Float, server_default=text("0"))
        boot_seconds = db.Column(db.Integer, server_default=text("0"))
        ts = db.Column(db.Integer, server_default=text("0"))

        #redis
        used_memory = db.Column(db.Integer, server_default=text("0"))
        used_memory_rss = db.Column(db.Integer, server_default=text("0"))
        connected_clients = db.Column(db.SmallInteger, server_default=text("0"))
        uptime_in_seconds = db.Column(db.Integer, server_default=text("0"))
        mem_fragmentation_ratio = db.Column(db.Float, server_default=text("0"))
        keyspace_hits = db.Column(db.Integer, server_default=text("0"))
        keyspace_misses = db.Column(db.Integer, server_default=text("0"))
        hits_ratio = db.Column(db.Float, server_default=text("0"))
        delta_hits_ratio = db.Column(db.Float, server_default=text("0"))

        def __init__(self, cpu=0.0, memory=0.0, load_avg='0', disk_usage=0.0, boot_seconds=0, ts=0):
            self.cpu = cpu
            self.memory = memory
            self.load_avg = load_avg
            self.disk_usage = disk_usage
            self.boot_seconds = boot_seconds
            self.ts = ts

        def __repr__(self):
            return "<ConsoleHost cpu: %s, memory:%s, load_avg:%s, disk_usage:%s, boot_seconds:%s, ts:%s>" % (
                self.cpu, self.memory, self.load_avg, self.disk_usage, self.boot_seconds, self.ts)

    db.create_all()
    yield ConsoleHost
    db.drop_all()
