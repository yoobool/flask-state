from flask_state.server.bind_id import send_id
from flask_state.server.language import return_language
from flask_state.server.response_methods import make_response_content
from flask_state.server.host_status import row2dict
from flask_state.server import MsgCode
from flask import json
import flask


def test_bind_id(app):
    with app.test_request_context():
        assert json.loads(send_id(1, 1).data) == json.loads(make_response_content(MsgCode.ERROR_TYPE).data)

        assert json.loads(send_id().data).get('code') == json.loads(make_response_content().data).get('code')


def test_make_response_content(app):
    with app.test_request_context():
        assert type(make_response_content(MsgCode.SUCCESS)) == flask.Response


def test_return_language(app):
    with app.test_request_context():
        assert json.loads(return_language(1).data) == json.loads(
            make_response_content(MsgCode.NOT_SUPPORT_LANGUAGE).data)

        assert json.loads(return_language('a').data) == json.loads(
            make_response_content(MsgCode.NOT_SUPPORT_LANGUAGE).data)

        assert json.loads(return_language('English').data).get('code') == json.loads(
            make_response_content(MsgCode.SUCCESS).data).get('code')


def test_query_console_host(app, db, host):
    @app.route('/')
    def index():
        query_result = host.query.first()
        host_dict = row2dict(query_result)
        return make_response_content(data=host_dict)

    @app.route('/add', methods=['POST'])
    def add():
        form = flask.request.form
        todo = host(form['cpu'], form['memory'], form['load_avg'], form['disk_usage'], form['boot_seconds'],
                    form['ts'])
        db.session.add(todo)
        db.session.commit()
        return 'added'

    c = app.test_client()
    c.post('/add', data=dict(cpu='1', memory='2', load_avg='3', disk_usage='4', boot_seconds='5', ts='6'))
    rv = c.get('/')
    res = json.loads(rv.data)
    assert isinstance(res, dict)
    assert res['data'].get('cpu') == 1
    assert res['data'].get('memory') == 2
    assert res['data'].get('load_avg') == '3'
    assert res['data'].get('disk_usage') == 4
    assert res['data'].get('boot_seconds') == 5
    assert res['data'].get('ts') == 6
