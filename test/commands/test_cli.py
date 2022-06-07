import os
from pathlib import Path

import pytest

from pipcx.const import COMMAND_NOT_FOUND_ERROR
from pipcx.main import CLI, main


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


@pytest.fixture
def cli():
    return CLI()


def test_main_command_help(monkeypatch, capsys, cli):
    monkeypatch.setattr("sys.argv", ["pipcx", "init", '-h'])
    output = cli.print_help()
    assert 'init' in output


def test_main_cli_get_arg(monkeypatch, cli):
    monkeypatch.setattr("sys.argv", ["pipcx", "init", '-h'])
    assert cli.get_arg(3) is None
