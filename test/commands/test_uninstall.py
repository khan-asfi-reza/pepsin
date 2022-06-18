from test.utils import command_path, get_installed_libs_in_venv

import pytest

from pipcx.commands.install import Command as InstallCommand
from pipcx.commands.uninstall import Command as UninstallCommand
from pipcx.config import PipcxConfig


@pytest.fixture
def install_command():
    return InstallCommand()


@pytest.fixture
def uninstall_command():
    return UninstallCommand()


def test_uninstall_command(uninstall_command, install_command):
    conf = PipcxConfig()
    conf.update(venv="test_uninstall_venv")
    install_command.run(["pipcx", "install", "flask"])
    conf = PipcxConfig()
    assert conf.libraries == ["flask"]
    libraries = get_installed_libs_in_venv("test_uninstall_venv")
    assert "flask" in libraries
    uninstall_command.run(["pipcx", "uninstall", "flask"])
    conf = PipcxConfig()
    assert conf.libraries == []
    libraries = get_installed_libs_in_venv("test_uninstall_venv")
    assert "flask" not in libraries
