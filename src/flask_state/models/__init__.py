from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String

from ..conf.config import Config
from ..migrate import upgrade
from ..utils.logger import logger

db = SQLAlchemy()


class AlembicVersion(db.Model):
    __bind_key__ = Config.DEFAULT_BIND_SQLITE
    __tablename__ = "alembic_version"

    version_num = db.Column(String(32), unique=True)

    __table_args__ = (
        db.PrimaryKeyConstraint("version_num"),
        db.Index("alembic_version_pkc", version_num),
    )


class _Migrate(object):
    def __init__(self, db, **kwargs):
        self.db = db
        self.configure_args = kwargs


def model_init_app(app):
    with app.app_context():
        db.init_app(app)
        app.extensions["migrate"] = _Migrate(db)
        tables = [table.name for table in db.get_tables_for_bind(bind=Config.DEFAULT_BIND_SQLITE)]
        try:
            if tables:
                if Config.ALEMBIC_VERSION not in tables:
                    upgrade(app)
                else:
                    is_new = db.session.query(AlembicVersion.version_num == Config.DB_VERSION).first()
                    if not is_new:
                        upgrade(app)
        except Exception as e:
            logger.error(e)
            pass
        db.create_all(bind=Config.DEFAULT_BIND_SQLITE, app=app)
