from src.flask_state.conf import config
from src.flask_state.utils import constants


def test_constant():
    """
    Test whether the constant value is correct
    """
    constant = config.Config
    operating_system = constants.OperatingSystem
    assert constant.CPU_PERCENT_INTERVAL == 0
    assert constant.DEFAULT_BIND_SQLITE == "flask_state_sqlite"
    assert operating_system.WINDOWS_SYSTEM == "Windows"
    assert operating_system.UNIX_SYSTEM == "Unix"


def test_days_scope():
    """
    Test whether milliseconds can be correctly obtained within the date range
    """
    days_scope = constants.TimeConstants.DAYS_SCOPE
    for day in days_scope:
        try:
            _value = constants.DaysMilliseconds[days_scope.get(day)].value
        except Exception as e:
            assert isinstance(TypeError, e)


def test_http_method():
    """
    Test whether the HTTP method is correct
    """
    http_method_list = ["POST", "GET", "PUT", "DELETE", "PATCH"]
    for method in http_method_list:
        assert method == constants.HttpMethod[method].value
