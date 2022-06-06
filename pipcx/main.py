import functools
import os
import pkgutil
import sys
from importlib import import_module

from pipcx.base import Base
from pathlib import Path

from pipcx.version import get_version

path = Path(__file__).resolve().parent


def find_commands():
    """
    Finds commands located in the commands directory
    """
    function_directory = os.path.join(path, "commands")

    return [
        name
        for _, name, is_pkg in pkgutil.iter_modules([function_directory])
        if not is_pkg and not name.startswith("_")
    ]


def load_command_class(name) -> Base:
    """
    Every Command module has a Command class, which will be imported
    :return Command Class
    """
    module = import_module(f"pipcx.commands.{name}")
    return module.Command()


@functools.lru_cache(maxsize=None)
def get_commands():
    """
    Set of commands that will be returned
    :return: set of commands
    """
    commands = {name for name in find_commands()}
    return commands


class Main:

    def __init__(self):
        self.argv = sys.argv[:]
        self.program_name = os.path.basename(self.argv[0])

        if self.program_name == "__main__.py":
            self.program_name = "python -m pipcx"

        try:
            self.command = self.argv[1]
        except IndexError:
            self.command = "help"

    def execute(self):

        command_class = load_command_class(self.command)
        if self.argv[1:] == '--version':
            sys.stdout.write(get_version() + "\n")

        else:
            command_class.run(self.argv)


def main():
    runner = Main()
    runner.execute()


main()
