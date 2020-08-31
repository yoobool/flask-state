from flask_state.server import default_conf_obj


def test_default_conf_obj():
    class_obj = default_conf_obj

    assert isinstance(class_obj.ID_NAME, tuple)
    assert isinstance(class_obj.LANGUAGE, str)
    assert isinstance(class_obj.SECS, int)
    assert isinstance(class_obj.ADDRESS, str)

    class_obj.set_id_name(1)
    assert class_obj.ID_NAME == ('1', True)

    class_obj.set_language(1)
    assert class_obj.LANGUAGE == '1'

    class_obj.set_secs(1)
    assert class_obj.SECS == 60

    class_obj.set_address(1)
    assert class_obj.ADDRESS == 'sqlite:///1'
