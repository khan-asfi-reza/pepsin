from subprocess import CalledProcessError

import pytest

from pipcx.commands.install import Command
from pipcx.schema import PipcxConfig
from pipcx.utils import write_file, read_file
from test.utils import command_path


@pytest.fixture
def install_command():
    return Command()


def test_install(install_command, monkeypatch):
    monkeypatch.setattr("pipcx.utils.base.pip3_install", lambda _: _)
    install_command.run(["pipcx", "install", "django", "flask", "-r", "requirements.txt"])
    conf = PipcxConfig()
    configs = conf.format_config()
    assert configs.get("libraries") == ["django", "flask"]


def test_with_requirements(install_command, monkeypatch):
    def pip3_install(package):
        raise CalledProcessError(1, "Test")

    monkeypatch.setattr("pipcx.utils.base.pip3_install", lambda _: pip3_install(_))
    write_file("req.txt", "\n".join(["test", "django"]))
    install_command.run(["pipcx", "install", "-r", "req.txt"])
    read = read_file("pipcx.failed.log")
    assert "test" in read
