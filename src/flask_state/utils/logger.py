import io
import logging
import os
import sys
import traceback

from ..utils.constants import AnsiColor, LogLevels

if hasattr(sys, "_getframe"):

    def currentframe():
        return sys._getframe(3)


else:

    def currentframe():
        try:
            raise Exception
        except Exception:
            return sys.exc_info()[2].tb_frame.f_back


_srcfile = os.path.normcase(currentframe.__code__.co_filename)


# Logger object decorator
class LoggingWrap:
    def __init__(self):
        self.logger = None

    def set(self, logger_instance):
        self.logger = logger_instance

    def info(self, msg, *args, **kwargs):
        if self.logger and hasattr(self.logger, "info") and callable(self.logger.info):
            self.logger.info(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        if self.logger and hasattr(self.logger, "warning") and callable(self.logger.warning):
            self.logger.warning(msg, *args, **kwargs)

    def debug(self, msg, *args, **kwargs):
        if self.logger and hasattr(self.logger, "debug") and callable(self.logger.debug):
            self.logger.debug(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        if self.logger and hasattr(self.logger, "error") and callable(self.logger.error):
            self.logger.error(msg, *args, **kwargs)

    def exception(self, msg, *args, exc_info=True, **kwargs):
        self.logger.exception(msg, *args, exc_info=exc_info, **kwargs)


# flask_state default logger object
class DefaultLogger:
    def __init__(self):
        self.level_to_color = {
            LogLevels.INFO: AnsiColor.GREEN,
            LogLevels.WARNING: AnsiColor.YELLOW,
            LogLevels.ERROR: AnsiColor.RED,
            LogLevels.EXCEPTION: AnsiColor.RED,
        }
        self.logger = logging.getLogger("flask_state")
        self.stream_handler = logging.StreamHandler(sys.stdout)
        self.logger.addHandler(self.stream_handler)
        self.logger.setLevel(logging.INFO)
        self.logger.findCaller = DefaultLogger.find_caller

    @staticmethod
    def find_caller(stack_info=False, stacklevel=1):
        """
        Overwrite
        Find the stack frame of the caller so that we can note the source
        file name, line number and function name.
        """
        f = currentframe()

        # On some versions of IronPython, currentframe() returns None if
        # IronPython isn't run with -X:Frames.
        if f is not None:
            f = f.f_back
        rv = "(unknown file)", 0, "(unknown function)", None
        while hasattr(f, "f_code"):
            co = f.f_code
            filename = os.path.normcase(co.co_filename)

            if filename == _srcfile or "flask_state" not in filename:
                f = f.f_back
                continue
            sinfo = None
            if stack_info:
                sio = io.StringIO()
                sio.write("Stack (most recent call last):\n")
                traceback.print_stack(f, file=sio)
                sinfo = sio.getvalue()
                if sinfo[-1] == "\n":
                    sinfo = sinfo[:-1]
                sio.close()
            rv = co.co_filename, f.f_lineno, co.co_name, sinfo
            break
        return rv

    def adaptive(self, text, level):
        return "\033[{}m".format(self.level_to_color.get(level, AnsiColor.GREEN)) + text + "\033[0m"

    @staticmethod
    def red(text):
        return "\033[31m" + text + "\033[0m"

    @staticmethod
    def green(text):
        return "\033[32m" + text + "\033[0m"

    @staticmethod
    def yellow(text):
        return "\033[33m" + text + "\033[0m"

    @staticmethod
    def white(text):
        return "\033[37m" + text + "\033[0m"

    def info(self, msg, *args, **kwargs):
        self.update_color(LogLevels.INFO)
        self.logger.info(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        self.update_color(LogLevels.WARNING)
        self.logger.warning(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        self.update_color(LogLevels.ERROR)
        self.logger.error(msg, *args, **kwargs)

    def exception(self, msg, *args, exc_info=True, **kwargs):
        self.update_color(LogLevels.EXCEPTION)
        self.logger.exception(msg, *args, exc_info=exc_info, **kwargs)

    def update_color(self, level):
        formatter = logging.Formatter(self.get_color(level))
        self.stream_handler.setFormatter(formatter)
        self.logger.addHandler(self.stream_handler)

    def get_color(self, level):
        return (
            DefaultLogger.green("%(asctime)s ")
            + DefaultLogger.red("| ")
            + self.adaptive("%(levelname)s ", level)
            + DefaultLogger.red("| ")
            + DefaultLogger.white("%(module)s")
            + DefaultLogger.red(":")
            + DefaultLogger.white("%(funcName)s")
            + DefaultLogger.red(":")
            + DefaultLogger.white("%(lineno)d ")
            + DefaultLogger.red("- ")
            + self.adaptive("%(message)s", level)
        )

    def get(self):
        return self.logger


logger = LoggingWrap()
