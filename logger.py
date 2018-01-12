import os
import time

class Logger:
    """ Class logger

    Args:
        log_file (String): name of the file where write log

    Attributes:
        _file (String): name of the file where write lo
        _fd (Int): file descriptor of the logger

    """
    def __init__(self, log_file):
        self._file = log_file
        self._fd = -1

    def __enter__(self):
        """ Function that open the log file
        
        Args:
            No param
        Returns:
            No return
        Raises:
            print when file fail to open
        """
        try:
            self._fd = os.open(self._file, os.O_CREAT | os.O_APPEND | os.O_WRONLY)
            return self._fd
        except:
            print("Unable to open log_file %s" & self._file)

    def __exit__(self, type, value, traceback):
        """ Function that close the log file
        
        Args:
            No param
        Returns:
            No return
        Raises:
            No raises
        """
        if self._fd != -1:
            os.close(self._fd)

    @staticmethod
    def logger(func, *args, **kwargs):
        """ Function that execute function
        
        Args:
            param1 (Function) : function that need to be executed
            param2 (*args) : argument of the function
            param3 (*kargs) : option of the function
        Returns:
            wrapper () : /!\ ?? je ne comprend pas cette partie ??
        Raises:
            no raises
        """
        pass
        def wrapper(*args, **kwarsg):
            backup = 0
            os.dup2(1, backup)
            with Logger() as fd:
                os.dup2(fd, 1)
                ret = func(*args, **kwargs)
            os.dup2(backup, 1)
            return ret
        return wrapper

    @staticmethod
    def entry(msg, log_file="taskmaster.log"):
        """ Function that send message to all program launch
        
        Args:
            param1 (String) : message that need to be send
        Returns:
            No return
        Raises:
            no raises
        """
        with Logger(log_file) as fd:
            os.write(fd, bytes("[{}] {}\n".format(time.ctime(), msg), 'UTF-8'))
