import sys
from abc import ABC, abstractmethod
from argparse import ArgumentParser
from io import TextIOBase

from pipcx.version import get_version


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
        style_func = style_func or self.style_func
        self._out.write(style_func(msg))


class InvalidCommandError(Exception):
    """
    Exception class indicating a problem while executing a management
    command.
    """
    def __init__(self, return_code=1, *args):
        self.return_code = return_code
        super().__init__(*args)


class Base(ABC):
    def __init__(self):
        self.stdout = OutputWrapper(sys.stdout)
        self.stderr = OutputWrapper(sys.stderr)

    def setup_parser(self, program_name, command):
        parser = ArgumentParser(
            prog=f"{program_name} {command}"
        )
        parser.add_argument(
            "--version",
            action="version",
            version=get_version(),
        )
        self.add_argument(parser)
        return parser

    def print_help(self, program_name, command):
        self.setup_parser(program_name, command).print_help()

    def add_argument(self, parser):
        pass

    @abstractmethod
    def execute(self, *args, **kwargs):
        pass

    def run(self, argv):
        parser = self.setup_parser(argv[0], argv[1])
        options = vars(parser.parse_args(argv[2:]))
        args = options.pop("args", ())
        try:
            self.execute(*args, **options)
        except InvalidCommandError as e:
            self.stderr.write("%s: %s" % (e.__class__.__name__, e))
            sys.exit(e.return_code)
