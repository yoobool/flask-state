from flask_state.server import default_conf_obj


def test_default_conf_obj():
    class_obj = default_conf_obj

    assert isinstance(class_obj.SECS, int)
    assert isinstance(class_obj.ADDRESS, str)

    class_obj.set_secs(1)
    assert class_obj.SECS == 60

    class_obj.set_address(1)
    assert class_obj.ADDRESS == 'sqlite:///1'
