from flask import json

from src.flask_state import query_console_status


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
