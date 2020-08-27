from .base import db


def model_init_app(app):
    db.init_app(app)
    with app.app_context():
        create_db(db)


def create_db(db_obj):
    db_obj.create_all()
