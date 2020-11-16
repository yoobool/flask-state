from src.flask_state.conf import config


def test_constant():
    """
    Test whether the constant value is correct
    """
    constant = config.Constant
    assert 60 == constant.DEFAULT_SECONDS
    assert 60 == constant.MIN_SECONDS
    assert 1 == constant.REDIS_TIMEOUT
    assert 0 == constant.CPU_PERCENT_INTERVAL
    assert "flask_state_sqlite" == constant.DEFAULT_BIND_SQLITE
    assert "sqlite:///flask_state_host.db" == constant.DEFAULT_DB_URL
    assert "Windows" == constant.WINDOWS_SYSTEM
    assert "Unix" == constant.UNIX_SYSTEM
    assert 11 == constant.MIN_ADDRESS_LENGTH
    assert 480 == constant.MAX_RETURN_RECORDS


def test_days_scope():
    """
    Test whether milliseconds can be correctly obtained within the date range
    """
    for day in config.DAYS_SCOPE:
        try:
            value = config.DaysMilliseconds[config.DAYS_SCOPE.get(day)].value
        except Exception as e:
            assert type(e) == KeyError


def test_http_method():
    """
    Test whether the HTTP method is correct
    """
    http_method_list = ["POST", "GET", "PUT", "DELETE", "PATCH"]
    for method in http_method_list:
        assert method == config.HttpMethod[method].value
