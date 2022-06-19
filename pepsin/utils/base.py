"""
Contains Base utility that is required to run the pepsin CLI Class
"""
import enum
import functools
import os
import pkgutil
from importlib import import_module
from pathlib import Path
from sys import platform

from pepsin.base import Base

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
    module = import_module(f"pepsin.commands.{name}")
    return module.Command()


@functools.lru_cache(maxsize=None)
def get_commands():
    """
    Set of commands that will be returned
    :return: set of commands
    """
    commands = set(find_commands())
    return commands


def check_file_exists(file):
    """
    Checks if file exists in working directory
    """
    return os.path.isfile(os.path.join(os.getcwd(), file))


def get_default(target, replace):
    """
    Checks if something is null or empty otherwise return the replacement
    """
    return replace if not target else target


def read_file(file):
    """
    Safely read File and return text
    """
    try:
        with open(file, "r", encoding="utf-8") as __file:
            return __file.read()
    except FileNotFoundError:
        return ""


def write_file(file, text):
    """
    Safely write file
    """
    with open(file, "w", encoding="utf-8") as __file:
        return __file.write(text)


def update_file(file, text):
    """
    Safely updates a file
    """
    read_text = read_file(file)
    write_file(file, read_text + "\n" + text)


def check_dir_exists(*paths):
    """
    Checks if a particular directory exists or not
    Args:
        *paths: Paths to join and check for directory existence

    Returns:

    """
    return os.path.isdir(os.path.join(*paths))


class OSEnum(enum.Enum):
    """
    OS Enum
    """

    LINUX = "linux"
    WIN = "win"
    OSX = "darwin"


def get_os(plt=platform) -> OSEnum:
    """
    Returns System OS Platform name
    """
    __os = OSEnum.LINUX
    if plt in ["linux", "linux2"]:
        __os = OSEnum.LINUX
    elif plt == "darwin":
        __os = OSEnum.OSX
    elif plt in ["win32", "cygwin"]:
        __os = OSEnum.WIN

    return __os
