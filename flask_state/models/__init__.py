from .base import db


def model_init_app(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()
