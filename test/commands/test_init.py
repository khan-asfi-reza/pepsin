import os
from collections import deque
from pathlib import Path

import pytest

from pipcx.commands.init import Command as InitCommand
import shutil

from test.utils import make_multiple_inputs


@pytest.fixture
def init_command():
    return InitCommand()


@pytest.fixture
def path():
    path = Path(__file__).resolve().parent / 'temp'
    os.chdir(path=path)
    return path


def test_init_with_option_args(init_command, path, monkeypatch):
    monkeypatch.setattr("builtins.input", make_multiple_inputs(
        deque(["my_proj", "mit", "author", "name@name.com"])))
    init_command.run(["pipcx", "init", "--venv=testvenv"])
    assert os.path.isdir("testvenv")
    assert os.path.isdir("my_proj")
    assert os.path.isfile("pipcx.yaml")
    assert os.path.isfile("my_proj/main.py")
    shutil.rmtree(path / 'testvenv')
    shutil.rmtree(path / 'my_proj')
    os.remove("pipcx.yaml")


