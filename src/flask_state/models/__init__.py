from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, func

from ..conf.config import Config
from ..migrate import upgrade
from ..utils.file_lock import file_lock
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


class _Migrate:
    def __init__(self, db, **kwargs):
        self.db = db
        self.configure_args = kwargs


def model_init_app(app):
    with app.app_context():
        db.init_app(app)
        app.extensions["migrate"] = _Migrate(db)
        engine = db.get_engine(app=app, bind=Config.DEFAULT_BIND_SQLITE)
        db.create_all(bind=Config.DEFAULT_BIND_SQLITE, app=app)
        upgrade_raw_db(app)


@file_lock("db")
def upgrade_raw_db(app):
    record = db.session.query(AlembicVersion).first()
    try:
        if not record:
            for version in Config.VERSION_LIST:
                try:
                    upgrade(app, version)
                except:
                    version_record = db.session.query(AlembicVersion).first()
                    if version_record:
                        version_record.version_num = version
                        db.session.commit()
                    else:
                        alembic_version = AlembicVersion(version_num=version)
                        db.session.add(alembic_version)
                        db.session.commit()
        elif record.version_num != Config.LATEST_VERSION:
            upgrade(app)
    except Exception as e:
        logger.exception(str(e))
        db.session.rollback()
