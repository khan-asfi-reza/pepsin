"""
Handles virtual environment related actions
"""
import enum
import os
from sys import platform

import pkg_resources

from pipcx.utils.base import pip3_install, python_sys_execute


class OSEnum(enum.Enum):
    """
    OS Enum
    """
    LINUX = 'linux'
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


def install_venv() -> None:
    """
    Installs virtualenv library
    """
    required = {'virtualenv'}
    installed = {pkg.key for pkg in pkg_resources.working_set}
    missing = required - installed
    if missing:
        pip3_install(*missing)


def initialize_venv(venv_dir: str = "venv"):
    """
    Initializes virtualenv directory
    """
    python_sys_execute("virtualenv", venv_dir)


def activate_venv(venv_dir: str = "venv"):
    """
    Activates virtualenv
    """
    sys_os = get_os()
    working_dir = os.getcwd()
    if sys_os == OSEnum.WIN:
        os.system(os.path.join(working_dir, f'{venv_dir}/scripts/activate'))
    else:
        os.system(f'source {venv_dir}/bin/activate')
