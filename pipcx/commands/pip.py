"""
PIP Command module
"""
from argparse import ArgumentParser

from pipcx.base import Base
from pipcx.pyhandler import PyHandler


class Command(Base):
    """
    Executes Pip command
    Examples:
        `pip --h` now can be written as
        `pipcx pip --h`
    """

    def add_argument(self, parser: ArgumentParser):
        parser.add_argument(
            "command", metavar="<command>", nargs="*", help="Pip command, IE: freeze"
        )

    def execute(self):
        py_handler = PyHandler(skip_venv=True)
        if self.command_data.get("command"):
            py_handler.pip_execute(*self.argv)
