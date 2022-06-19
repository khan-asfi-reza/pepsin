from test.utils import command_path, set_subprocess
from urllib.error import URLError

import pytest

from pepsin.commands.upgrade import Command
from pepsin.config import PepsinConfig
from pepsin.utils import write_file


@pytest.fixture
def upgrade_command():
    return Command()


def test_install(upgrade_command):
    upgrade_command.run(
        ["pepsin", "upgrade", "flask", "pip", "-r", "requirements.txt"]
    )
    conf = PepsinConfig()
    configs = conf.format_config()
    assert configs.get("libraries") == ["flask"]


def test_install_with_req(upgrade_command):
    write_file("requirements.txt", "\n".join(["django", "flask"]))
    upgrade_command.run(["pepsin", "upgrade", "-r", "requirements.txt"])
    conf = PepsinConfig()
    assert conf.libraries == ["django", "flask"]


def test_install_without_req(upgrade_command):
    conf = PepsinConfig()
    conf.update(libraries=["django", "flask"])
    upgrade_command.run(["pepsin", "upgrade"])
    assert conf.libraries == ["django", "flask"]


def test_upgrade_pip_fail(upgrade_command, monkeypatch, capsys):
    def raise_urlopen_error(*args, **kwargs):
        raise URLError("TEST")

    monkeypatch.setattr("urllib.request.urlopen", raise_urlopen_error)
    upgrade_command.run(["pepsin", "upgrade", "pip"])
    assert "Unable to upgrade" in capsys.readouterr().err
