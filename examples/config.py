from flask import Flask
from flask_state import init_app, default_conf_obj


def settint_app():
    app = Flask(__name__)
    default_conf_obj.set_id_name('console_machine_status', True)
    default_conf_obj.set_language('English')
    default_conf_obj.set_address('console_machine_status', 0)
    default_conf_obj.set_secs(20)
    init_app(app)
    return app
