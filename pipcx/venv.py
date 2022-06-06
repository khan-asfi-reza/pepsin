import enum
import os
from sys import platform

import pkg_resources

from pipcx.utils import pip3_install, python_sys_execute


class OSEnum(enum.Enum):
    LINUX = 'linux'
    WIN = "win"
    OSX = "darwin"


def get_os():
    if platform == "linux" or platform == "linux2":
        return OSEnum.LINUX
    elif platform == "darwin":
        return OSEnum.OSX
    elif platform == "win32" or platform == "cygwin":
        return OSEnum.WIN


def install_venv():
    required = {'virtualenv'}
    installed = {pkg.key for pkg in pkg_resources.working_set}
    missing = required - installed
    if missing:
        pip3_install(*missing)


def initialize_venv():
    python_sys_execute("virtualenv", "venv")


def activate_venv():
    sys_os = get_os()
    working_dir = os.getcwd()
    if sys_os == OSEnum.WIN:
        os.system(os.path.join(working_dir, 'venv/scripts/activate'))
    else:
        os.system('source venv/bin/activate')