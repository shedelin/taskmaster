import os
from threading import Thread
from program import Program
from logger import Logger

class Seeker(Thread):
    """
    CREATED = False
        INSTANCE = None
        RUNNING_PROGS = 0

        def __new__(cls):
            if not Seeker.CREATED:
                print("seeker Created")
                Seeker.INSTANCE = super(Seeker, cls).__new__(cls)
            return Seeker.INSTANCE
    
	 Class Seeker

		use of super on the class Thread
    """
    def __init__(self):
        super(Seeker, self).__init__()

    def run(self):
        while True:
            if Program.SEM._value < 10:
                try:
                    pid, exit_status = os.wait()
                except ChildProcessError:
                    pass
                prg = Program.getPrgByPid(pid)
                if not prg:
                    print(pid, exit_status)
                Logger.entry("Process (%d)%s has finish [%d]" % (pid, prg.getName(), exit_status))
                prg.finish(exit_status)
            else:
                break

    # def __enter__(self):
    #     Seeker.RUNNING_PROGS += 1

    # def __exit__(self, tye, value, traceback):
    #     """
    #     Seeker.RUNNING_PROGS -= 1

    #     Function that run the thread
    #     Args:
    #         No param
    #     Returns:
    #         No return
    #     Raises:
    #         No raise
    #     """
    #     while Program.RUNNING_PROGS:
    #         pid, exit_status = os.wait()
    #         print(pid, exit_status)
    #         prg = Program.getPrgByPid(pid)
    #         Logger.entry("Process (%d)%s has finish [%d]" % (pid, prg.getName(), exit_status))
    #         prg.finish(exit_status)
