import sys
from abc import ABC, abstractmethod
from argparse import ArgumentParser
from io import TextIOBase


class OutputWrapper(TextIOBase):
    """
    Wrapper around stdout/stderr
    """

    @property
    def style_func(self):
        return self._style_func

    @style_func.setter
    def style_func(self, style_func):
        if style_func and self.isatty():
            self._style_func = style_func
        else:
            self._style_func = lambda x: x

    def __init__(self, out, ending="\n"):
        self._out = out
        self.style_func = None
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


class CommandError(Exception):
    """
    Exception class indicating a problem while executing a management
    command.

    If this exception is raised during the execution of a management
    command, it will be caught and turned into a nicely-printed error
    message to the appropriate output stream (i.e., stderr); as a
    result, raising this exception (with a sensible description of the
    error) is the preferred way to indicate that something has gone
    wrong in the execution of a command.
    """

    def __init__(self, *args, returncode=1, **kwargs):
        self.returncode = returncode
        super().__init__(*args, **kwargs)


class CommandParser(ArgumentParser):
    """
    Customized ArgumentParser class to improve some error messages and prevent
    SystemExit in several occasions, as SystemExit is unacceptable when a
    command is called programmatically.
    """

    def __init__(
            self, *, missing_args_message=None, called_from_command_line=None, **kwargs
    ):
        self.missing_args_message = missing_args_message
        self.called_from_command_line = called_from_command_line
        super().__init__(**kwargs)

    def parse_args(self, args=None, namespace=None):
        # Catch missing argument for a better error message
        if self.missing_args_message and not (
                args or any(not arg.startswith("-") for arg in args)
        ):
            self.error(self.missing_args_message)
        return super().parse_args(args, namespace)

    def error(self, message):
        if self.called_from_command_line:
            super().error(message)
        else:
            raise CommandError("Error: %s" % message)


class Base(ABC):
    def __init__(self):
        self.stdout = OutputWrapper(sys.stdout)
        self.stderr = OutputWrapper(sys.stderr)

    def get_version(self):
        return '1'

    def setup_parser(self):
        parser = ArgumentParser()
        parser.add_argument(
            "--version",
            action="version",
            version=self.get_version(),
        )
        return parser

    @abstractmethod
    def execute(self):
        pass

    def run(self):
        parser = self.setup_parser()
        options = parser.parse_args(sys.argv[2:])
        cmd_options = vars(options)
        # Move positional args out of options to mimic legacy optparse
        args = cmd_options.pop("args", ())

