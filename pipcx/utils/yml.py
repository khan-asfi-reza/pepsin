import copy
from collections import namedtuple

import yaml


def dict_to_yaml(_dict, filename):
    with open(filename, "w") as file:
        yaml.dump(_dict, file)


def yaml_to_dict(yaml_file) -> dict:
    with open(yaml_file, "r") as file:
        return yaml.load(file, yaml.Loader)


class YamlConfigLoader:
    __config_dict = {}

    def __init__(self, filename):
        self.filename = filename
        self.load()
        self.config = namedtuple("Config", self.__config_dict.keys())(*self.__config_dict.values())

    def get_config(self):
        return self.config

    def load(self):
        self.__config_dict = yaml_to_dict(self.filename)


class YamlConfigGenerator:
    __config = {}

    def __init__(self, filename, **config):
        self.filename = filename
        self.__config = config

    def append(self, **config_data):
        self.__config.update(**config_data)

    def remove(self, key):
        return self.__config.pop(key)

    def read(self):
        return copy.deepcopy(self.__config)

    def generate(self):
        dict_to_yaml(self.__config, self.filename)
