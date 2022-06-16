"""
Contains Base utility that is required to run the pipcx CLI Class
"""
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
    commands = set(find_commands())
    return commands


def pip3_install(package: str) -> None:
    """
    Installs package via pip3
    """
    subprocess.run(['pip3', 'install', package])


def pip3_upgrade(package: str):
    """
    Upgrade package via pip3
    """
    subprocess.run(["pip3", "install", "--upgrade", package])


def python_sys_execute(*command) -> None:
    """
    Does python -m <command>
    """
    python = sys.executable
    subprocess.run([python, '-m', *command])


def python_exec(*command):
    """
    Executes python script
    """
    python = sys.executable
    subprocess.run([python, '-m', *command])


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
        with open(file, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        return ""


def write_file(file, text):
    """
    Safely write file
    """
    with open(file, "w", encoding="utf-8") as file:
        return file.write(text)


def update_file(file, text):
    """
    Safely updates a file
    """
    read_text = read_file(file)
    write_file(file, read_text + '\n' + text)
