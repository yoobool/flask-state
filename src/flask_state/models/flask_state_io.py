# -*- coding: utf-8 -*-

from sqlalchemy import func
from sqlalchemy.dialects.mysql import BIGINT, DATETIME, INTEGER
from sqlalchemy.sql import text

from ..conf.config import Config
from . import db


class FlaskStateIO(db.Model):
    __bind_key__ = Config.DEFAULT_BIND_SQLITE
    __tablename__ = "flask_state_io"

    id = db.Column(INTEGER(unsigned=True), autoincrement=True)
    create_time = db.Column(DATETIME, server_default=func.now())
    update_time = db.Column(
        DATETIME, server_default=func.now(), onupdate=func.now()
    )

    # network
    net_sent = db.Column(BIGINT(unsigned=True), server_default=text("0"))
    net_recv = db.Column(BIGINT(unsigned=True), server_default=text("0"))
    packets_sent = db.Column(BIGINT(unsigned=True), server_default=text("0"))
    packets_recv = db.Column(BIGINT(unsigned=True), server_default=text("0"))

    # disk
    disk_read = db.Column(BIGINT(unsigned=True), server_default=text("0"))
    disk_write = db.Column(BIGINT(unsigned=True), server_default=text("0"))
    read_count = db.Column(BIGINT(unsigned=True), server_default=text("0"))
    write_count = db.Column(BIGINT(unsigned=True), server_default=text("0"))

    ts = db.Column(BIGINT(unsigned=True), server_default=text("0"))
    __table_args__ = (
        db.PrimaryKeyConstraint("id"),
        db.Index("idx_ct", create_time.desc()),
        {
            "extend_existing": True,
        },
    )

    def __repr__(self):
        return "<FlaskStateIO net_sent: {}, net_recv:{}, disk_read:{}, disk_write:{}>".format(
            self.net_sent,
            self.net_recv,
            self.disk_read,
            self.disk_write,
        )
