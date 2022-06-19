from test.utils import command_path, get_installed_libs_in_venv

import pytest

from pepsin.commands.install import Command as InstallCommand
from pepsin.commands.uninstall import Command as UninstallCommand
from pepsin.config import PepsinConfig


@pytest.fixture
def install_command():
    return InstallCommand()


@pytest.fixture
def uninstall_command():
    return UninstallCommand()


def test_uninstall_command(uninstall_command, install_command):
    conf = PepsinConfig()
    conf.update(venv="test_uninstall_venv")
    install_command.run(["pepsin", "install", "flask"])
    conf = PepsinConfig()
    assert conf.libraries == ["flask"]
    libraries = get_installed_libs_in_venv("test_uninstall_venv")
    assert "flask" in libraries
    uninstall_command.run(["pepsin", "uninstall", "flask"])
    conf = PepsinConfig()
    assert conf.libraries == []
    libraries = get_installed_libs_in_venv("test_uninstall_venv")
    assert "flask" not in libraries
