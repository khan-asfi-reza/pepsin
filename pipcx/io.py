import sys
from io import TextIOBase


class OutputWrapper(TextIOBase):
    """
    Wrapper around stdout/stderr
    """

    def __init__(self, out, ending="\n"):
        self._out = out
        self.ending = ending

    def __getattr__(self, name):
        return getattr(self._out, name)

    def flush(self):
        if hasattr(self._out, "flush"):
            self._out.flush()

    def isatty(self):
        return hasattr(self._out, "isatty") and self._out.isatty()

    def write(self, msg="", style_func=None, ending=None):
        ending = self.ending if ending is None else ending
        if ending and not msg.endswith(ending):
            msg += ending
        self._out.write(msg)


class IOBase:
    def __init__(self):
        self.stdout = OutputWrapper(sys.stdout)
        self.stderr = OutputWrapper(sys.stderr)

    def output(self, text):
        self.stdout.write(text)

    def output_flush(self):
        self.stdout.flush()

    def error(self, text):
        self.stderr.write(text)

    def error_flush(self):
        self.stderr.flush()