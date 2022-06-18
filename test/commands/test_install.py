import subprocess
import time
from test.utils import command_path, set_subprocess

import pytest

from pipcx.commands.install import Command
from pipcx.config import PipcxConfig
from pipcx.utils import check_file_exists, write_file


@pytest.fixture
def install_command():
    return Command()


def test_install(install_command):
    install_command.run(
        ["pipcx", "install", "flask", "-r", "requirements.txt"]
    )
    conf = PipcxConfig()
    configs = conf.format_config()
    assert configs.get("libraries") == ["flask"]


def test_install_with_req(install_command):
    write_file("requirements.txt", "\n".join(["django", "flask"]))
    install_command.run(["pipcx", "install", "-r", "requirements.txt"])
    conf = PipcxConfig()
    assert conf.libraries == ["django", "flask"]


def test_install_without_req(install_command):
    conf = PipcxConfig()
    conf.update(libraries=["django", "flask"])
    install_command.run(["pipcx", "install"])
    assert conf.libraries == ["django", "flask"]
