import os
import shutil
from pathlib import Path

import pytest

from pepsin.utils import OSEnum, check_dir_exists, get_os


def make_multiple_inputs(inputs: list):
    """provides a function to call for every input requested."""

    def next_input(_):
        """provides the first item in the list."""
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
    path = Path(__file__).resolve().parent / "temp"
    os.chdir(path=path)
    return path


@pytest.fixture(autouse=True)
def set_subprocess(monkeypatch):
    def check_call(*args, **kwargs):
        pass

    monkeypatch.setattr("subprocess.check_call", check_call)
    yield


@pytest.fixture(autouse=True)
def command_path():
    path = Path(__file__).resolve().parent / "temp"
    os.chdir(path=path)
    try:
        if check_dir_exists(path, "__TEST__"):
            safe_remove_dir("__TEST__")
        os.mkdir("__TEST__")
    except PermissionError:
        pass
    os.chdir(path=path / "__TEST__")
    yield
    os.chdir(path=path)
    safe_remove_dir("__TEST__")
    safe_remove_dir("venv")
    safe_remove_file("pepsin.yaml")
    safe_remove_file("pepsin.failed.log")


def get_installed_libs_in_venv(venv_name):
    if get_os() == OSEnum.WIN:
        dirs = os.listdir(os.path.join(venv_name, "lib", "site-packages"))
    else:
        py_dir = os.listdir(
            os.path.join(
                venv_name,
                "lib",
            )
        )
        dirs = os.listdir(
            os.path.join(venv_name, "lib", py_dir[0], "site-packages")
        )

    return dirs
