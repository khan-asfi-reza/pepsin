import os
import subprocess
from pathlib import Path

import pytest

from pipcx.const import COMMAND_NOT_FOUND_ERROR
from pipcx.main import CLI, main
from pipcx.utils import get_os, OSEnum
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
