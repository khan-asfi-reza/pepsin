import os
from test.utils import command_path, get_installed_libs_in_venv

import pytest

from pipcx.commands.install import Command
from pipcx.config import PipcxConfig
from pipcx.utils import OSEnum, check_dir_exists, check_file_exists, get_os


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
    dirs = get_installed_libs_in_venv("install_venv")
    assert "requests" in dirs
