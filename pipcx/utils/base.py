import functools
import os
import pkgutil
import subprocess
import sys
from importlib import import_module
from pathlib import Path

from pipcx.base import Base

ROOT = Path(__file__).resolve().parent


def find_commands():
    """
    Finds commands located in the commands directory
    """
    function_directory = os.path.join(ROOT, "../commands")

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


def pip3_install(package: str) -> None:
    """
    Installs package via pip3
    """
    subprocess.check_call(['pip3', 'install', package])


def python_sys_execute(*command) -> None:
    """
    Does python -m <command>
    """
    python = sys.executable
    subprocess.check_call([python, '-m', *command])
