import flask
from flask import _app_ctx_stack


def test_basic_insert(app, db, host):
    @app.route('/')
    def index():
        query_result = host.query.first()
        query_name = ['cpu', 'memory', 'load_avg', 'disk_usage', 'boot_seconds', 'ts']
        result = ''
        for x in query_name:
            result += str(int(getattr(query_result, x)))
        return result

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
    assert rv.data == b'123456'


def test_query_recording(app, db, host):
    with app.test_request_context():
        host_obj = host('1', '2')
        db.session.add(host_obj)
        db.session.flush()
        host.load_avg = '3'
        db.session.commit()
        query = getattr(_app_ctx_stack.top, 'sqlalchemy_queries', [])[0]
        assert query.parameters[0] == 1.0
        assert query.parameters[1] == 2.0
