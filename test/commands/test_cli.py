import os
import subprocess
from pathlib import Path
import sys
import pytest
from unittest.mock import MagicMock
from pipcx.const import COMMAND_NOT_FOUND_ERROR
from pipcx.main import CLI, main
from pipcx.utils import pip3_install, get_os, OSEnum, activate_venv, install_venv
from pipcx.utils.spinner import Spinner
from pipcx.version import get_version


@pytest.fixture
def path():
    path = Path(__file__).resolve().parent / 'temp'
    os.chdir(path=path)
    return path


def test_main_help(monkeypatch, capsys):
    monkeypatch.setattr("sys.argv", ["pipcx", "help"])
    main()
    assert 'Available commands' in capsys.readouterr().out


def test_main_command_error(monkeypatch, capsys):
    monkeypatch.setattr("sys.argv", ["pipcx", "ins"])
    main()
    assert COMMAND_NOT_FOUND_ERROR in capsys.readouterr().err


def test_main_command_help(monkeypatch):
    cli = CLI(["pipcx", "init", '-h'])
    output = cli.print_help()
    assert 'init' in output


def test_main_cli_get_arg(monkeypatch):
    cli = CLI(["pipcx", "init", '-h'])
    assert cli.get_arg(3) is None


def test_version(capsys):
    cli = CLI(["pipcx", "--version"])
    cli.execute()
    assert get_version() in capsys.readouterr().out


def test_command_help():
    cli = CLI(["__main__.py"])
    cli.execute()
    assert 1


def test_spinner():
    spinner = Spinner(sequence="TEST", message="Message")
    spinner.start()
    spinner.stop()
    assert 1


def test_default_spinner():
    spinner = Spinner()
    spinner.start()
    spinner.stop()
    assert 1


def check_all(lst=None):
    pass


def test_pip3_install(monkeypatch):
    try:
        pip3_install("os")
    except subprocess.CalledProcessError as e:
        assert e.returncode == 1


def test_sys_platform():
    # Test Linux system
    platform_os = get_os("linux")
    assert platform_os == OSEnum.LINUX
    # Test windows system
    platform_os = get_os("darwin")
    assert platform_os == OSEnum.OSX
    # Test windows system
    platform_os = get_os("win32")
    assert platform_os == OSEnum.WIN


def test_activate_venv_linux(monkeypatch):
    monkeypatch.setattr("pipcx.utils.venv.get_os", lambda: OSEnum.LINUX)
    monkeypatch.setattr("os.system", lambda _: _)
    activate_venv("test")


def test_activate_venv_windows(monkeypatch):
    monkeypatch.setattr("pipcx.utils.venv.get_os", lambda: OSEnum.WIN)
    monkeypatch.setattr("os.system", lambda _: _)
    activate_venv("test")


def test_install_venv(monkeypatch):
    monkeypatch.setattr("pkg_resources.working_set", {})
    monkeypatch.setattr("pipcx.utils.base.pip3_install", lambda _: _)
    install_venv()
