from src.flask_state import default_conf


def test_default_conf():
    test_conf = default_conf

    assert isinstance(test_conf.SECS, int)
    assert isinstance(test_conf.ADDRESS, str)

    test_conf.set_secs(1)
    assert test_conf.SECS == 60

    test_conf.set_address(1)
    assert test_conf.ADDRESS == 'sqlite:///1'
