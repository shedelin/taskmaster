import os
import sys
from logger import Logger
from copy import deepcopy
import threading

def protected(func, *args, **kwargs):
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except FileNotFoundError:
            print("[{}] No such file or directory: '{}'".format(func.__mame__, args[0]))
        except PermissionError:
            print("[{}] Permission Denied: '{}'".format(func.__mame__, args[0]))
    return wrapper

class Program:
    """ Class Program

    Args:
        name (String): name of the program
        params (String) : parameters of the program

    Attributes:
        _status (String) : status of the program
        _name (String): name of the program
        _params (String) : parameters of the program
        _pid (Int) : pid of the program
        _fdou (Int) : file descriptors of the file where write the output of the program
        _fderr (Int) : file descriptors of the file where write the errors of the program

    Getters & setters:
        getName
        getStatus
        getPid

    """
    PRECONFIG_PARAMS = [
        "env",
        "stderr",
        "stdout",
        "workingdir"
        ]

    PROGRAMS = []
    SEM = threading.Semaphore(10)

    class AttributeNotFound(Exception):
        def __init__(self, value):
            super(Program.AttributeNotFound, self).__init__(value)
            self._value = value

    @staticmethod
    def getPrgByPid(pid):
        """ Function that get and return the program by id
        
        Args:
            param1 (Int) : id of the program we search
        Returns:
            prg (Program) : the program with id we want
        Raises:
            print when file fail to open
        """
        for prg in Program.PROGRAMS:
            if pid == prg.getPid():
                return prg

    def __init__(self, name, params):
        self._status = "Waiting"
        self._name = name
        self._params = params
        self._pid = 0
        self._fdout = None
        self._fderr = None
        self._environ = deepcopy(os.environ)

    def _close(self):
        """ Function that the file descriptors of program
        
        Args:
            No param
        Returns:
            No return
        Raises:
            No raise
        """
        if self._fdout:
            os.close(self._fdou)
        if self._fderr:
            os.close(self._fderr)

    def updateConfig(self, params):
        """ Function that update params of the program
        
        Args:
            param1 () : new params
        Returns:
            No return
        Raises:
            No raise
        """
        self._params = params

    def getAutoStart(self):
        return self._params.get("autostart", False)

    def print_params(self):
        """ Function that print the parameters of the program
        
        Args:
            No param
        Returns:
            No return
        Raises:
            No raise
        """
        output = []
        for attr_name, attr_value in self._params.items():
            output.append("\t\033[1m{:15}:\033[0m {}".format(attr_name, attr_value))
        return "\n".join(output)

    def finish(self, exit_status):
        """ Function that stop program
        
        Args:
            param1 () : exit status
        Returns:
            No return
        Raises:
            No raise
        """
        Program.SEM.release()
        if os.WIFEXITED(exit_status):
            self._pid = 0
            self._status = "Finished [%d]" % exit_status
        elif os.WIFSIGNALED(exit_status):
            self._status = "Interrupted [%d]" % exit_status
        else:
            self._status = "Not handled [%d]" % exit_status

    def execute(self):
        """ Function that execute the program
        
        Args:
            No param
        Returns:
            No return
        Raises:
            cmd not set
            File not found or Permission denied
        """
        if not "cmd" in self._params:
            raise "'cmd' not set"
        cmd_array = self._params["cmd"].split()
        if os.access(cmd_array[0], os.F_OK | os.X_OK):
            self._pid = os.fork()
            if self._pid == 0:
                self._apply_preconfig()
                Logger.entry("Process (%d)%s has started." % (os.getpid(), self._name))
                os.execve(cmd_array[0], cmd_array, self._environ)
                print("Execve error")
                Program.SEM.release()
                sys.exit(-1)
            else:
                Program.SEM.acquire()
                self._status = "Running"
        else:
            print("Command not found: {}".format(cmd_array[0]))

    def kill(self, sig):
        """ Function that kill the program
        
        Args:
            param1 (Int) : signal needed to kill the program
        Returns:
            No return
        Raises:
            No raise
        """
        if self._pid != 0:
            os.kill(self._pid, sig)

    def getName(self):
        return self._name

    def getStatus(self):
        return self._status

    def getPid(self):
        return self._pid

    def _apply_preconfig(self):
        """ Function that fill the PRECONFIG_PARAMS of the program
        
        Args:
            No param
        Returns:
            No return
        Raises:
            No raise
        """
        for attr in Program.PRECONFIG_PARAMS:
            if attr in self._params.keys():
                apply_fct = getattr(self, "_{}__{}".format(Program.__name__, attr))
                if apply_fct:
                    apply_fct(self._params[attr])
                else:
                    raise Program.AttributeNotFound(attr)

    @protected
    def __stdout(self, output_file):
        self._fdout = os.open(output_file, os.O_WRONLY | os.O_CREAT)
        os.dup2(self._fdout, 1)

    @protected
    def __stderr(self, output_file):
        self._fderr = os.open(output_file, os.O_WRONLY | os.O_CREAT)
        os.dup2(self._fderr, 2)

    def stdout(self, output_file):
        """ Function that open the file where right the output of the program
        
        Args:
            param1 (String) : Name of the file where write
        Returns:
            No return
        Raises:
            No raise
        """
        self._fdout = os.open(output_file, os.O_WRONLY | os.O_CREAT)
        os.dup2(self._fdout, 1)

    def stderr(self, output_file):
        """ Function that open the file where right the errors of the program
        
        Args:
            param1 (String) : Name of the file where write
        Returns:
            No return
        Raises:
            No raise
        """
        self._fderr = os.open(output_file, os.O_WRONLY | os.O_CREAT)
        os.dup2(self._fderr, 2)

    @protected
    def __workingdir(self, working_dir):
        os.chdir(working_dir)

    @protected
    def __env(self, env_var):
        for key, value in env_var.items():
            self._environ[key] = str(value)
