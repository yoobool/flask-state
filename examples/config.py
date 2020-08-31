from flask import Flask
from flask_state import init_app, default_conf_obj


def settint_app():
    app = Flask(__name__)

    # Redis conf
    app.config['REDIS_CONF'] = {
        'REDIS_STATUS': True,
        'REDIS_HOST': '192.168.0.2',
        'REDIS_PORT': 16379,
        'REDIS_PASSWORD': 'fish09'
    }

    # set conf
    default_conf_obj.set_language('English')

    import os
    path_ = os.getcwd() + '/test.db'
    default_conf_obj.set_address(path_)

    default_conf_obj.set_secs(20)

    # use init_app initial configuration
    init_app(app)
    return app
