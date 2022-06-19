import os
from pathlib import Path
from test.utils import safe_remove_file

import pytest

from pepsin.config import PepsinConfig


@pytest.fixture
def path():
    path = Path(__file__).resolve().parent / "temp"
    os.chdir(path=path)
    return path


@pytest.fixture(autouse=True)
def run_around_tests():
    yield
    path = Path(__file__).resolve().parent / "temp"
    os.chdir(path=path)
    safe_remove_file("pepsin.yaml")


def test_yaml_config(path):
    conf = PepsinConfig()
    conf.update(name="Project")
    config = conf.format_config()
    assert config.get("name") == "Project"
    assert conf.config_exists()
    safe_remove_file("pepsin.yaml")


def test_yaml_libraries():
    conf = PepsinConfig()
    conf.update_libraries([])
    conf.update_libraries(["test==2.3.5"])
    assert "test==2.3.5" in conf.format_config().get("libraries")
    conf.update_libraries(["test==2.3.6"])
    assert "test==2.3.6" in conf.format_config().get("libraries")
    safe_remove_file("pepsin.yaml")


def test_init_config():
    conf = PepsinConfig()
    conf.initialize_config()
    assert conf.config_exists()
