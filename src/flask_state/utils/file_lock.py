import os
import platform
import time

from ..conf.config import Constant

SYSTEM = Constant.WINDOWS_SYSTEM if platform.system() == Constant.WINDOWS_SYSTEM else Constant.UNIX_SYSTEM
if SYSTEM == Constant.UNIX_SYSTEM:
    import fcntl


class Lock:
    @staticmethod
    def get_file_lock():
        return FileLock()


class FileLock:
    def __init__(self):
        lock_file = '821e9dab54fec92e3d054b3367a50b70d328caed'
        if SYSTEM == Constant.WINDOWS_SYSTEM:
            lock_dir = os.environ['tmp']
        else:
            lock_dir = '/tmp'

        self.file = f'{lock_dir}{os.sep}{lock_file}'
        self._fn = None
        self.release()

    def acquire(self):
        if SYSTEM == Constant.WINDOWS_SYSTEM:
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
        if SYSTEM == Constant.WINDOWS_SYSTEM:
            if os.path.exists(self.file):
                os.remove(self.file)
        else:
            if self._fn:
                try:
                    self._fn.close()
                except Exception as e:
                    raise e
