import logging
import sys


# Logger object decorator
class LoggingWrap:
    def __init__(self):
        self.logger = None

    def set(self, logger_instance):
        self.logger = logger_instance

    def info(self, msg, *args, **kwargs):
        if self.logger and hasattr(self.logger, 'info') and callable(self.logger.info):
            self.logger.info(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        if self.logger and hasattr(self.logger, 'warning') and callable(self.logger.warning):
            self.logger.warning(msg, *args, **kwargs)

    def debug(self, msg, *args, **kwargs):
        if self.logger and hasattr(self.logger, 'debug') and callable(self.logger.debug):
            self.logger.debug(msg, *args, **kwargs)

    def exception(self, msg, *args, exc_info=False, **kwargs):
        if self.logger and hasattr(self.logger, 'exception') and callable(self.logger.exception):
            self.logger.exception(msg, *args, exc_info=exc_info, **kwargs)


# flask_state default logger object
class DefaultLogger:
    def __init__(self):
        self.logger = logging.getLogger('flask_state')
        log_format = DefaultLogger.green('%(asctime)s ') + DefaultLogger.red('| ') + DefaultLogger.yellow(
            '%(levelname)s ') + DefaultLogger.red('| ') + DefaultLogger.white(
            '%(handlerFileName)s') + DefaultLogger.red(':') + DefaultLogger.white(
            '%(handlerFuncName)s') + DefaultLogger.red(':') + DefaultLogger.white(
            '%(handlerLine)d ') + DefaultLogger.red('- ') + DefaultLogger.green('%(message)s')
        stream_handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(log_format)
        stream_handler.setFormatter(formatter)
        self.logger.addHandler(stream_handler)
        self.logger.setLevel(logging.INFO)

    @staticmethod
    def red(text):
        return '\033[31m' + text + '\033[0m'

    @staticmethod
    def green(text):
        return '\033[32m' + text + '\033[0m'

    @staticmethod
    def yellow(text):
        return '\033[33m' + text + '\033[0m'

    @staticmethod
    def white(text):
        return '\033[37m' + text + '\033[0m'

    def get(self):
        return self.logger


logger = LoggingWrap()
