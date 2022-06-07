import os
from pathlib import Path

import pytest

from pipcx.commands.init import Command as InitCommand
import shutil


@pytest.fixture
def init_command():
    return InitCommand()


@pytest.fixture
def path():
    path = Path(__file__).resolve().parent / 'temp'
    os.chdir(path=path)
    return path


def test_init_with_option_args(init_command, path):
    init_command.run(["pipcx", "init", "--venv=testvenv"])
    assert os.path.isdir("testvenv") is True
    shutil.rmtree(path / 'testvenv')


def test_init_with_var_arg(init_command, path):
    init_command.run(["pipcx", "init", "testvenv"])
    assert os.path.isdir("testvenv") is True
    shutil.rmtree(path / 'testvenv')
