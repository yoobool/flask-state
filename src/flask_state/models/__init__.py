from flask_sqlalchemy import SQLAlchemy

from ..conf.config import Constant

db = SQLAlchemy()


def model_init_app(app):
    db.init_app(app)
    with app.app_context():
        db.create_all(bind=Constant.DEFAULT_BIND_SQLITE)
