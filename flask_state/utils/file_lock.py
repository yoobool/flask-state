import os
import time

WINDOWS = 'windows'
UNIX = 'unix'
SYSTEM = None

try:
    import fcntl

    SYSTEM = UNIX
except:
    SYSTEM = WINDOWS


class Lock:
    @staticmethod
    def get_file_lock():
        return FileLock()


class FileLock:
    def __init__(self):
        lock_file = 'MONITOR_LOCK'
        if SYSTEM == WINDOWS:
            lock_dir = os.environ['tmp']
        else:
            lock_dir = '/tmp'

        self.file = '%s%s%s' % (lock_dir, os.sep, lock_file)
        self._fn = None
        self.release()

    def acquire(self):
        if SYSTEM == WINDOWS:
            while os.path.exists(self.file):
                time.sleep(0.01)  # wait 10ms
                continue

            with open(self.file, 'w') as f:
                f.write('1')
        else:
            self._fn = open(self.file, 'w')
            fcntl.flock(self._fn.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
            self._fn.write('1')

    def release(self):
        if SYSTEM == WINDOWS:
            if os.path.exists(self.file):
                os.remove(self.file)
        else:
            if self._fn:
                try:
                    self._fn.close()
                except Exception as e:
                    raise e
