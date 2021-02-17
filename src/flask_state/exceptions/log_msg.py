from . import ExceptionMsg


class ErrorMsg(ExceptionMsg):
    LACK_SQLITE = {
        "msg": "app.config must to set up SQLALCHEMY_BINDS and bind flask_state_sqlite",
        "level": "error",
    }
    ERROR_ADDRESS = {
        "msg": "Incorrect address format, Set the format to: sqlite:///path",
        "level": "error",
    }
    NO_ACCESS = {
        "msg": "Path has no access, make sure you have access to the path",
        "level": "error",
    }
    DATA_TYPE_ERROR = {"msg": "Data type format error", "level": "error"}
    ACQUIRED_LOCK_FAILED = {"msg": "File lock not obtained", "level": "error"}
    ERROR_CRON = {
        "msg": "Wrong cron parameter, make sure the parameters you enter meet the format requirements",
        "level": "error",
    }
    RUN_TIME_ERROR = {
        "msg": "Exceed the maximum allowable execution time",
        "level": "error",
    }


class WarningMsg(ExceptionMsg):
    TIME_SMALL = {"msg": "Setting the recording time is too short", "level": "warning"}
    LACK_REDIS = {"msg": "Redis module is not installed", "level": "warning"}


class InfoMsg(ExceptionMsg):
    INSERT_SUCCESS = {"msg": "Insert status", "level": "info"}
    DELETE_SUCCESS = {"msg": "Delete expired records", "level": "info"}
    QUERY_SUCCESS = {"msg": "Query status", "level": "info"}
    GET_YESTERDAY = {"msg": "Query yesterday status", "level": "info"}
    ACQUIRED_LOCK = {"msg": "Acquired file lock successfully", "level": "info"}
