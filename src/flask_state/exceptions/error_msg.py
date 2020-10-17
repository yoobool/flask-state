from . import ExceptionMsg


class ErrorMsg(ExceptionMsg):
    LACK_SQLITE = {'msg': 'app.config must to set up SQLALCHEMY_BINDS and bind flask_state_sqlite', 'level': 'error'}
    ERROR_ADDRESS = {'msg': 'Incorrect address format, Set the format to: sqlite:///path', 'level': 'error'}


class WarningMsg(ExceptionMsg):
    DATA_TYPE_ERROR = {'msg': 'Data type format error', 'level': 'warning'}
    NO_ACCESS = {'msg': 'Path has no access, now use the default address instead(sqlite:///flask_state_host.db)',
                 'level': 'warning'}
