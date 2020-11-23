from src.flask_state.conf import config
from src.flask_state.utils import constants


def test_constant():
    """
    Test whether the constant value is correct
    """
    constant = config.Config
    operating_system = constants.OperatingSystem
    assert 1 == constant.REDIS_CONNECT_TIMEOUT
    assert 5 == constant.REDIS_TIMEOUT
    assert 0 == constant.CPU_PERCENT_INTERVAL
    assert "flask_state_sqlite" == constant.DEFAULT_BIND_SQLITE
    assert "Windows" == operating_system.WINDOWS_SYSTEM
    assert "Unix" == operating_system.UNIX_SYSTEM
    assert 480 == constant.MAX_RETURN_RECORDS


def test_days_scope():
    """
    Test whether milliseconds can be correctly obtained within the date range
    """
    days_scope = constants.TimeConstants.DAYS_SCOPE
    for day in days_scope:
        try:
            value = constants.DaysMilliseconds[days_scope.get(day)].value
        except Exception as e:
            assert type(e) == KeyError


def test_http_method():
    """
    Test whether the HTTP method is correct
    """
    http_method_list = ["POST", "GET", "PUT", "DELETE", "PATCH"]
    for method in http_method_list:
        assert method == constants.HttpMethod[method].value
