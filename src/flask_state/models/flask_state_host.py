# -*- coding: utf-8 -*-

from sqlalchemy import String, func
from sqlalchemy.dialects.mysql import BIGINT, DATETIME, FLOAT, INTEGER, SMALLINT
from sqlalchemy.sql import text

from ..conf.config import Config
from . import db


class FlaskStateHost(db.Model):
    __bind_key__ = Config.DEFAULT_BIND_SQLITE
    __tablename__ = "flask_state_host"

    id = db.Column(INTEGER(unsigned=True), autoincrement=True)
    create_time = db.Column(DATETIME, server_default=func.now())
    update_time = db.Column(DATETIME, server_default=func.now(), onupdate=func.now())

    # host
    cpu = db.Column(FLOAT(unsigned=True), server_default=text("0"))
    cpus = db.Column(String(128), server_default="[]")
    memory = db.Column(FLOAT(unsigned=True), server_default=text("0"))
    load_avg = db.Column(String(32), server_default="")
    disk_usage = db.Column(FLOAT(unsigned=True), server_default=text("0"))
    boot_seconds = db.Column(INTEGER(unsigned=True), server_default=text("0"))
    ts = db.Column(BIGINT(unsigned=True), server_default=text("0"))

    # redis
    used_memory = db.Column(INTEGER(unsigned=True), server_default=text("0"))
    used_memory_rss = db.Column(INTEGER(unsigned=True), server_default=text("0"))
    connected_clients = db.Column(SMALLINT(unsigned=True), server_default=text("0"))
    uptime_in_seconds = db.Column(INTEGER(unsigned=True), server_default=text("0"))
    mem_fragmentation_ratio = db.Column(FLOAT(unsigned=True), server_default=text("0"))
    keyspace_hits = db.Column(INTEGER(unsigned=True), server_default=text("0"))
    keyspace_misses = db.Column(INTEGER(unsigned=True), server_default=text("0"))
    hits_ratio = db.Column(FLOAT(unsigned=True), server_default=text("0"))
    delta_hits_ratio = db.Column(FLOAT(unsigned=True), server_default=text("0"))

    __table_args__ = (
        db.PrimaryKeyConstraint("id"),
        db.Index("idx_ts", ts.desc()),
        {
            "extend_existing": True,
        },
    )

    def __repr__(self):
        return "<FlaskStateHost cpu: {}, memory:{}, load_avg:{}, disk_usage:{}, boot_seconds:{}, ts:{}>".format(
            self.cpu,
            self.memory,
            self.load_avg,
            self.disk_usage,
            self.boot_seconds,
            self.ts,
        )
