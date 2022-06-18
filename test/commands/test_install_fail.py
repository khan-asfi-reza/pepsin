import os

import pytest

from pipcx.commands.install import Command
from pipcx.config import PipcxConfig
from pipcx.utils import check_file_exists, check_dir_exists, get_os, OSEnum

from test.utils import command_path


@pytest.fixture
def install_command():
    return Command()


def test_fail_requirement(install_command, monkeypatch):
    install_command.run(["pipcx", "install", "test2test"])
    assert check_file_exists("pipcx.failed.log")


def test_install_command_within_dir(install_command):
    conf = PipcxConfig()
    conf.update(libraries=["requests"], venv="install_venv")
    install_command.run(["pipcx", "install"])
    assert check_dir_exists("install_venv")
    if get_os() == OSEnum.WIN:
        dirs = os.listdir(os.path.join("install_venv", "lib", "site-packages"))
    else:
        py_dir = os.listdir(os.path.join("install_venv", "lib", ))
        dirs = os.listdir(os.path.join("install_venv", "lib", py_dir[0], "site-packages"))

    assert "requests" in dirs
