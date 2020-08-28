from flask import json

from flask_state.controller.manager import bind_id2element, get_language, query_console_status
from flask_state.server import default_conf_obj


def test_bind_id(app):
    app.add_url_rule('/v0/state/bindid', endpoint='state_bind_id', view_func=bind_id2element, methods=['GET', 'POST'])

    c = app.test_client()

    def id_and_assert(code='200'):
        rv = c.post('/v0/state/bindid')
        result = json.loads(rv.data)
        assert result.get('code') == code
        assert isinstance(result.get('data'), dict)
        assert 'circular' in result['data'] and 'id_name' in result['data']
        assert result.get('msg') == 'ID sent successfully'

    id_and_assert()

    default_conf_obj.set_id_name()
    id_and_assert()

    rv = c.get('/v0/state/bindid')
    result = json.loads(rv.data)
    assert result.get('code') == '10002'


def test_language(app):
    app.add_url_rule('/v0/state/language', endpoint='state_language', view_func=get_language, methods=['GET', 'POST'])

    c = app.test_client()

    def language_and_assert(code='200', msg='SUCCESS'):
        rv = c.post('/v0/state/language')
        result = json.loads(rv.data)
        assert result.get('code') == code
        assert result.get('msg') == msg

    language_and_assert()

    default_conf_obj.set_language()
    language_and_assert('10003', 'Language not supported')

    default_conf_obj.set_language(0)
    language_and_assert('10003', 'Language not supported')

    default_conf_obj.set_language('aa')
    language_and_assert('10003', 'Language not supported')

    rv = c.get('/v0/state/language')
    result = json.loads(rv.data)
    assert result.get('code') == '10002'


def test_query_host(app, host):
    app.add_url_rule('/v0/state/hoststatus', endpoint='state_host_status', view_func=query_console_status,
                     methods=['GET', 'POST'])

    c = app.test_client()

    def host_and_assert(code='200', msg='Search success', data=None):
        data = json.dumps(data)
        rv = c.post('/v0/state/hoststatus', data=data)
        result = json.loads(rv.data)
        assert result.get('code') == code
        assert result.get('msg') == msg

    host_and_assert('10005', 'JSON format is required')

    host_and_assert('10001', 'Exceeding the allowed query time range', {'1': '1'})

    host_and_assert(data={'timeQuantum': '1'})

    rv = c.get('/v0/state/hoststatus')
    result = json.loads(rv.data)
    assert result.get('code') == '10002'
