import os

import pytest

from pipcx.commands.init import Command as InitCommand
from pipcx.main import CLI
from test.utils import make_multiple_inputs, command_path


@pytest.fixture
def init_command():
    return InitCommand()


def test_init_with_option_args(init_command, monkeypatch):
    # Set input parameter
    monkeypatch.setattr("builtins.input", make_multiple_inputs(
        ["testproject", "mit", "author", "name@name.com"]))
    # Run the command
    init_command.run(["pipcx", "init", "--venv=testvenv"])
    # Check directories
    assert os.path.isdir("testvenv")
    assert os.path.isdir("testproject")
    assert os.path.isfile("pipcx.yaml")
    assert os.path.isfile("testproject/main.py")
    assert os.path.isfile("Readme.MD")
    assert os.path.isfile(".gitignore")


def test_init_with_predefined_files_no_input(init_command, monkeypatch):
    cli = CLI(["pipcx", "init", "testproject", "--venv=testvenv", "--no-input"])
    # Set input parameter
    os.mkdir("testproject")
    with open("testproject/main.py", "w") as file:
        file.write("print('Hello World')")
        file.close()
    # Run the command
    cli.execute()
    # Check directories
    assert os.path.isdir("testvenv")
    assert os.path.isdir("testproject")
    assert os.path.isfile("pipcx.yaml")
    assert os.path.isfile("testproject/main.py")
    assert os.path.isfile("Readme.MD")
    assert os.path.isfile(".gitignore")
    # Read if file has not been updated
    with open("testproject/main.py", "r") as file:
        assert "Hello World" in file.read()
        file.close()


def test_init_with_predefined_files(monkeypatch):
    cli = CLI(["pipcx", "init", "testproject", "--venv=testvenv"])
    # Set input parameter
    monkeypatch.setattr("builtins.input", make_multiple_inputs(
        ["mit", "author", "name@name.com"]))

    os.mkdir("testproject")
    with open("testproject/main.py", "w") as file:
        file.write("print('Hello World')")
        file.close()
    # Run the command
    cli.execute()
    # Check directories
    assert os.path.isdir("testvenv")
    assert os.path.isdir("testproject")
    assert os.path.isfile("pipcx.yaml")
    assert os.path.isfile("Readme.MD")
    assert os.path.isfile(".gitignore")
    assert os.path.isfile("testproject/main.py")
    # Read if file has not been updated
    with open("testproject/main.py", "r") as file:
        assert "Hello World" in file.read()
        file.close()
