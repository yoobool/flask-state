from src.flask_state.exceptions import error_code, log_msg


def test_msg_code():
    """
    Test whether the error code method is correct and whether the returned result is correct
    """
    for item in error_code.MsgCode:
        try:
            assert isinstance(item.get_msg(), str)
            assert isinstance(item.get_code(), int)
        except Exception as e:
            assert isinstance(type(e), AttributeError)


def test_log_msg():
    """
    Test whether the logger information acquisition method is correct and whether the level is correct
    """
    # error level
    for info in log_msg.ErrorMsg:
        try:
            assert isinstance(info.get_msg(), str)
            assert isinstance(info.get_level(), str)
        except Exception as e:
            assert isinstance(type(e), AttributeError)
        assert info.get_level() == "error"
        assert info.get_msg("error") == info.get_msg() + "error"

    # warning level
    for info in log_msg.WarningMsg:
        try:
            assert isinstance(info.get_msg(), str)
            assert isinstance(info.get_level(), str)
        except Exception as e:
            assert isinstance(type(e), AttributeError)
        assert info.get_level() == "warning"
        assert info.get_msg("warning") == info.get_msg() + "warning"

    # info level
    for info in log_msg.InfoMsg:
        try:
            assert isinstance(info.get_msg(), str)
            assert isinstance(info.get_level(), str)
        except Exception as e:
            assert isinstance(type(e), AttributeError)
        assert info.get_level() == "info"
        assert info.get_msg("info") == info.get_msg() + "info"
