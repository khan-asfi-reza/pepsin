import os
import shutil
from pathlib import Path

import pytest


@pytest.fixture(autouse=True)
def command_path():
    path = Path(__file__).resolve().parent / 'temp'
    os.chdir(path=path)
    os.mkdir("__TEST__")
    os.chdir(path=path / "__TEST__")
    yield
    os.chdir(path=path)
    safe_remove_dir("__TEST__")
    safe_remove_dir("venv")
    safe_remove_dir("pipcx.yaml")


def make_multiple_inputs(inputs: list):
    """ provides a function to call for every input requested. """

    def next_input(_):
        """ provides the first item in the list. """
        return inputs.pop(0)

    return next_input


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


@pytest.fixture
def temp_path():
    path = Path(__file__).resolve().parent / 'temp'
    os.chdir(path=path)
    return path
