import os
from test.utils import command_path

import pytest

from pepsin.pyhandler import PyHandler
from pepsin.utils import write_file


@pytest.fixture
def py_handler():
    return PyHandler()


def test_py_handler_python_exec(py_handler):
    write_file("py_init.py", "print('pepsin')")
    py_handler.python_execute("py_init.py")


def test_py_handler_pip_command(py_handler):
    py_handler.pip_execute("--h")


def test_py_handler_skip_venv():
    py_handler = PyHandler(skip_venv=True)
    py_handler.pip_execute("--h")
    assert not os.path.isdir("venv")
