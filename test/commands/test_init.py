import os
from collections import deque
from pathlib import Path

import pytest

from pipcx.commands.init import Command as InitCommand
import shutil

from pipcx.main import CLI
from test.utils import make_multiple_inputs


@pytest.fixture
def init_command():
    return InitCommand()


@pytest.fixture
def path():
    path = Path(__file__).resolve().parent / 'temp'
    os.chdir(path=path)
    return path


def safe_remove_dir(dir_path):
    try:
        shutil.rmtree(dir_path)
    except FileNotFoundError:
        pass


def safe_remove_file(file_path):
    try:
        os.remove(file_path)
    except FileNotFoundError:
        pass


@pytest.fixture(autouse=True)
def run_around_tests():
    yield
    path = Path(__file__).resolve().parent / 'temp'
    os.chdir(path=path)
    safe_remove_dir("testproject")
    safe_remove_dir("testvenv")
    safe_remove_file("pipcx.yaml")
    safe_remove_file("pytest.yaml")


def test_init_with_option_args(init_command, path, monkeypatch):
    # Set input parameter
    monkeypatch.setattr("builtins.input", make_multiple_inputs(
        deque(["testproject", "mit", "author", "name@name.com"])))
    # Run the command
    init_command.run(["pipcx", "init", "--venv=testvenv"])
    # Check directories
    assert os.path.isdir("testvenv")
    assert os.path.isdir("testproject")
    assert os.path.isfile("pipcx.yaml")
    assert os.path.isfile("testproject/main.py")
    # Remove test files
    shutil.rmtree(path / 'testvenv')
    shutil.rmtree(path / 'testproject')
    os.remove("pipcx.yaml")


def test_init_with_predefined_files(path, monkeypatch):
    cli = CLI(["pipcx", "init", "--venv=testvenv"])
    # Set input parameter
    monkeypatch.setattr("builtins.input", make_multiple_inputs(
        deque(["testproject", "mit", "author", "name@name.com"])))
    monkeypatch.setattr("sys.argv", ["pipcx", "init", "--venv=testvenv"])
    # Run the command
    os.mkdir("testproject")
    with open("testproject/main.py", "w") as file:
        file.write("print('Hello World')")
        file.close()

    cli.execute()
    # Check directories
    assert os.path.isdir("testvenv")
    assert os.path.isdir("testproject")
    assert os.path.isfile("pipcx.yaml")
    assert os.path.isfile("testproject/main.py")
    # Read if file has not been updated
    with open("testproject/main.py", "r") as file:
        assert "Hello World" in file.read()
        file.close()
    # Remove test files
    shutil.rmtree(path / 'testvenv')
    shutil.rmtree(path / 'testproject')
    os.remove("pipcx.yaml")
