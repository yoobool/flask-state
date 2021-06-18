import copy
import logging
from logging import config

from flask import app

from ..utils.constants import AnsiColor, LogLevels

BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, GREY = range(9)

RESET_SEQ = "\033[0m"
COLOR_SEQ = "\033[%dm"
BOLD_SEQ = "\033[1m"

COLOR_MAP = {
    logging.DEBUG: GREY,
    logging.INFO: WHITE,
    logging.WARNING: YELLOW,
    logging.CRITICAL: RED,
    logging.ERROR: RED,
}

FLASK_STATE = "flaskstate"


class ColorizeFormatter(logging.Formatter):
    def __init__(self, fmt=None, datefmt=None, style="%"):
        super(ColorizeFormatter, self).__init__(fmt, datefmt, style)

    def format(self, record: logging.LogRecord):
        color = COLOR_MAP.get(record.levelno)
        if not color:
            color = BLUE
        tmp = copy.copy(record)
        name_color = self._wrap_color(f"{tmp.name}", CYAN)
        funcName_color = self._wrap_color(f"{tmp.funcName}", CYAN)
        level_color = self._wrap_color(tmp.levelname, color)
        message_color = self._wrap_color(f"{tmp.msg}", GREEN)
        tmp.name = name_color
        tmp.funcName = funcName_color
        tmp.msg = message_color
        tmp.levelname = level_color
        return logging.Formatter.format(self, tmp)

    @staticmethod
    def _wrap_color(string: str, color):
        return COLOR_SEQ % (30 + color) + string + RESET_SEQ


def _has_config(logger):
    return (
        logger.level != logging.NOTSET
        or logger.handlers
        or logger.filters
        or not logger.propagate
    )


class LoggerAllocator:
    def __init__(self):
        self._logger = logging.getLogger(FLASK_STATE)

    @property
    def logger(self):
        return self._logger

    @logger.setter
    def logger(self, out_logger: logging.Logger = None):
        if out_logger:
            self._logger = out_logger
        elif not _has_config(self._logger):
            default_handler = logging.StreamHandler()
            default_handler.setFormatter(
                ColorizeFormatter(
                    fmt="%(asctime)s | %(levelname)-8s | %(name)s:%(funcName)s:%(lineno)d | %(message)s"
                )
            )
            self._logger.setLevel(logging.INFO)
            self._logger.addHandler(default_handler)


flask_logger = LoggerAllocator()
