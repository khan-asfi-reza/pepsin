import os
from test.utils import command_path, get_installed_libs_in_venv

import pytest

from pepsin.commands.install import Command
from pepsin.config import PepsinConfig
from pepsin.utils import OSEnum, check_dir_exists, check_file_exists, get_os


@pytest.fixture
def install_command():
    return Command()


def test_fail_requirement(install_command, monkeypatch):
    install_command.run(["pepsin", "install", "test2test"])
    assert check_file_exists("pepsin.failed.log")


def test_install_command_within_dir(install_command):
    conf = PepsinConfig()
    conf.update(libraries=["requests"], venv="install_venv")
    install_command.run(["pepsin", "install"])
    assert check_dir_exists("install_venv")
    dirs = get_installed_libs_in_venv("install_venv")
    assert "requests" in dirs
