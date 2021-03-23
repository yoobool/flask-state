# -*- coding: utf-8 -*-
import argparse
import os

from alembic import command
from alembic.config import Config as AlembicConfig

__all__ = ["upgrade", "downgrade"]


def get_config():
    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "migrations")
    config = AlembicConfig(os.path.join(path, "alembic.ini"))
    config.set_main_option("script_location", path)
    config.cmd_opts = argparse.Namespace()
    setattr(config.cmd_opts, "x", None)
    return config


def upgrade(app):
    config = get_config()
    with app.app_context():
        command.upgrade(config, "head")


def downgrade(app):
    config = get_config()
    with app.app_context():
        command.downgrade(config, "-1")
