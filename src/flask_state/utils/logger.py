class LoggingWrap:
    def __init__(self):
        self.logger = None

    def set(self, test):
        self.logger = test

    def warning(self, msg, *args, **kwargs):
        if self.logger and hasattr(self.logger, 'warning') and callable(self.logger.warning):
            self.logger.warning(msg, *args, **kwargs)

    def debug(self, msg, *args, **kwargs):
        if self.logger and hasattr(self.logger, 'debug') and callable(self.logger.debug):
            self.logger.debug(msg, *args, **kwargs)

    def exception(self, msg, *args, exc_info=True, **kwargs):
        if self.logger and hasattr(self.logger, 'exception') and callable(self.logger.exception):
            self.logger.exception(msg, *args, exc_info, **kwargs)


logger = LoggingWrap()
