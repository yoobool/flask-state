from . import ExceptionMsg


class ErrorMsg(ExceptionMsg):
    LACK_SQLITE = {'msg': 'app.config must to set up SQLALCHEMY_BINDS and bind flask_state_sqlite', 'level': 'error'}
    ERROR_ADDRESS = {'msg': 'Incorrect address format, Set the format to: sqlite:///path', 'level': 'error'}
    NO_ACCESS = {'msg': 'Path has no access, now use the default address instead(sqlite:///flask_state_host.db)',
                 'level': 'warning'}
    DATA_TYPE_ERROR = {'msg': 'Data type format error', 'level': 'warning'}


class WarningMsg(ExceptionMsg):
    TIME_SMALL = {'msg': 'Setting the recording time is too short', 'level': 'warning'}


class InfoMsg(ExceptionMsg):
    INSERT_SUCCESS = {'msg': 'Insert status', 'level': 'info'}
    QUERY_SUCCESS = {'msg': 'Query status', 'level': 'info'}
    GET_YESTERDAY = {'msg': 'Query yesterday status', 'level': 'info'}
