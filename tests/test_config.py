from src.flask_state import flask_state_conf


def test_flask_state_conf():
    test_conf = flask_state_conf

    assert isinstance(test_conf.SECS, int)
    assert isinstance(test_conf.ADDRESS, str)

    test_conf.set_secs(1)
    assert test_conf.SECS == 60

    test_conf.set_address(1)
    assert test_conf.ADDRESS == 'sqlite:///1'
