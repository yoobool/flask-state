import sqlalchemy as sa
from flask_sqlalchemy import SQLAlchemy

from ..conf.config import Config
from ..migrate import upgrade
from ..utils.logger import logger

db = SQLAlchemy()


class AlembicVersion(db.Model):
    __bind_key__ = Config.DEFAULT_BIND_SQLITE
    __tablename__ = "alembic_version"

    version_num = db.Column(sa.String(32), unique=True)

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
        tables = sa.inspect(engine).get_table_names()

        if Config.ALEMBIC_VERSION not in tables:
            AlembicVersion.__table__.create(engine)
        try:
            if tables:
                is_new = (
                    db.session.query(AlembicVersion)
                    .filter(AlembicVersion.version_num == Config.DB_VERSION)
                    .first()
                )
                if not is_new:
                    upgrade(app)
        except Exception as e:
            logger.exception(e)
        db.create_all(bind=Config.DEFAULT_BIND_SQLITE, app=app)
