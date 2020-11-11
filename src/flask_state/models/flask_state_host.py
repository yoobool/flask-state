from sqlalchemy import func
from sqlalchemy.sql import text

from ..conf.config import Constant
from . import db


# model
class FlaskStateHost(db.Model):
    __bind_key__ = Constant.DEFAULT_BIND_SQLITE
    __tablename__ = "flask_state_host"

    __table_args__ = (
        db.PrimaryKeyConstraint('id'),
        {
            'extend_existing': True,
        }
    )
    id = db.Column(db.Integer, autoincrement=True)
    create_time = db.Column(db.DateTime, server_default=func.now())
    update_time = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())

    # host
    cpu = db.Column(db.Float, server_default=text("0"))
    memory = db.Column(db.Float, server_default=text("0"))
    load_avg = db.Column(db.String(32), server_default="")
    disk_usage = db.Column(db.Float, server_default=text("0"))
    boot_seconds = db.Column(db.Integer, server_default=text("0"))
    ts = db.Column(db.Integer, server_default=text("0"))

    # redis
    used_memory = db.Column(db.Integer, server_default=text("0"))
    used_memory_rss = db.Column(db.Integer, server_default=text("0"))
    connected_clients = db.Column(db.SmallInteger, server_default=text("0"))
    uptime_in_seconds = db.Column(db.Integer, server_default=text("0"))
    mem_fragmentation_ratio = db.Column(db.Float, server_default=text("0"))
    keyspace_hits = db.Column(db.Integer, server_default=text("0"))
    keyspace_misses = db.Column(db.Integer, server_default=text("0"))
    hits_ratio = db.Column(db.Float, server_default=text("0"))
    delta_hits_ratio = db.Column(db.Float, server_default=text("0"))

    def __repr__(self):
        return "<FlaskStateHost cpu: {}, memory:{}, load_avg:{}, disk_usage:{}, boot_seconds:{}, ts:{}>".format(
            self.cpu, self.memory, self.load_avg, self.disk_usage, self.boot_seconds, self.ts)
