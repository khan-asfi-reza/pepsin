import functools
import os
import pkgutil
import sys
from importlib import import_module

from base import Base


def find_commands():
    """
    Finds commands located in the commands directory
    """
    function_directory = os.path.join("commands")
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
    module = import_module(f"commands.{name}")
    return module.Command()


@functools.lru_cache(maxsize=None)
def get_commands():
    """
    Set of commands that will be returned
    :return: set of commands
    """
    commands = {name for name in find_commands()}
    return commands


def run_command(name):
    if name in get_commands():
        klass = load_command_class(name)
        klass.execute()


run_command("execute")
