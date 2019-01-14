import signal
import subprocess
import threading


SIGNALS = dict((k, v) for v, k in reversed(sorted(signal.__dict__.items()))
           if v.startswith('SIG') and not v.startswith('SIG_'))


class Command:

    DEFAULT_ENV     = {}
    DEFAULT_TIMEOUT = 600.
    DEFAULT_STDIN   = subprocess.PIPE
    DEFAULT_STDOUT  = subprocess.PIPE
    DEFAULT_STDERR  = subprocess.PIPE

    def __init__(self, cmd, cwd, shell=True, env=DEFAULT_ENV,
                 stdin=DEFAULT_STDIN, stdout=DEFAULT_STDOUT,
                 stderr=DEFAULT_STDERR):
        self.cmd    = cmd
        self.cwd    = cwd
        self.env    = env
        self.ps     = None
        self.shell  = shell
        self.stderr = stderr
        self.stdin  = stdin
        self.stdout = stdout

    def open(self):
        return subprocess.Popen(self.cmd, shell=self.shell,
                                env=self.env, cwd=self.cwd,
                                stdin=self.stdin, stdout=self.stdout,
                                stderr=self.stderr)

    def run(self, instr=None, timeout=DEFAULT_TIMEOUT):

        def target():
            self.ps = subprocess.Popen(self.cmd, shell=self.shell,
                                       env=self.env, cwd=self.cwd,
                                       stdin=self.stdin, stdout=self.stdout,
                                       stderr=self.stderr)
            self.out, self.err = self.ps.communicate(input=instr)

        thread = threading.Thread(target=target)
        thread.start()
        thread.join(timeout)
        if thread.is_alive():
            self.ps.terminate()
            thread.join()

        if self.ps.returncode < 0:
            sig = SIGNALS[-self.ps.returncode]
        elif self.ps.returncode == 126:
            sig = 'Cannot execute command invoked'
        elif self.ps.returncode == 127:
            sig = 'Command not found'
        elif self.ps.returncode == 128:
            sig = 'Invalid argument to exit'
        elif self.ps.returncode - 128 in SIGNALS:
            sig = SIGNALS[self.ps.returncode - 128]
        else:
            sig = self.ps.returncode

        return sig, self.out.decode('utf-8'), self.err.decode('utf-8')
