import os
from pathlib import Path

import pytest
import yaml

from pipcx.utils import yaml_to_dict, dict_to_yaml, YAMLConfig


@pytest.fixture
def path():
    path = Path(__file__).resolve().parent / 'data'
    os.chdir(path=path)
    return path


def test_yaml_load():
    yaml_data = """
    data: Test
    name: pipcx
    """
    data = yaml.load(yaml_data, yaml.Loader)
    assert data["name"] == 'pipcx'


def test_load_yaml_data(path):
    data = yaml_to_dict("test.yaml")
    assert data.get("name") == 'Pipcx'


def test_load_dict_to_yaml(path):
    __dict = {"name": "Pipcx"}
    dict_to_yaml(__dict, "pytest.yaml")
    data = yaml_to_dict("pytest.yaml")
    assert data.get("name") == 'Pipcx'
    os.remove("pytest.yaml")


def test_yaml_config_loader(path):
    Config = YAMLConfig("test.yaml")
    assert Config.get("name") == "Pipcx"


def test_dict_to_yaml_config_loader(path):
    conf = YAMLConfig("pytest.yaml")
    conf.append(name="Pipcx")
    conf.append(number=12)
    assert conf.get("name") == "Pipcx"
    conf.remove("number")
    assert conf.get("number") is None
    conf.save()
    assert conf.get("name") == "Pipcx"
    os.remove("pytest.yaml")