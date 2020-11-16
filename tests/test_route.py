from flask import json

from src.flask_state.conf import config
from src.flask_state.controller import manager
from src.flask_state.models import model_init_app


def test_init_app(app):
    model_init_app(app)
    app.add_url_rule(
        "/v0/state/hoststatus",
        endpoint="state_host_status",
        view_func=manager.query_flask_state,
        methods=[config.HttpMethod.POST.value],
    )
    c = app.test_client()
    response = c.post(
        "/v0/state/hoststatus",
        data=json.dumps({"timeQuantum": 1}),
        content_type="application/json",
    )
    assert 200 == response.status_code
