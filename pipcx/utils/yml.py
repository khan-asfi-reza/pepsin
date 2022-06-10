"""
Handles Yaml Config and converts from yaml to dictionary or
dictionary to yaml
"""
import copy
from collections import namedtuple

import yaml


def dict_to_yaml(_dict, filename):
    """
    Converts dictionary to yaml
    _dict: Python dictionary or hash map
    filename: Name of yaml file
    """
    with open(filename, "w", encoding="utf-8") as file:
        yaml.dump(_dict, file)


def yaml_to_dict(filename) -> dict:
    """
    Converts yaml  to  dictionary
    filename: Name of yaml file
    """
    with open(filename, "r", encoding="utf-8") as file:
        return yaml.load(file, yaml.Loader)


class YamlConfigLoader:
    """
    Yaml Config Loader loads config data from a yaml file
    """
    __config_dict = {}

    def __init__(self, filename):
        self.filename = filename
        self.load()
        self.config = namedtuple("Config", self.__config_dict.keys())(*self.__config_dict.values())

    def get_config(self):
        """
        Returns config
        """
        return self.config

    def load(self):
        """
        Loads yaml file
        """
        self.__config_dict = yaml_to_dict(self.filename)


class YamlConfigGenerator:
    """
    Yaml Config Generator generates yaml file
    """
    __config = {}

    def __init__(self, filename, **config):
        self.filename = filename
        self.__config = config

    def append(self, **config_data):
        """
        Appends data in the config dictionary
        """
        self.__config.update(**config_data)

    def remove(self, key):
        """
        Removes data from config
        """
        return self.__config.pop(key)

    def read(self):
        """
        Create copy of config
        """
        return copy.deepcopy(self.__config)

    def generate(self):
        """
        Generates yaml file
        """
        dict_to_yaml(self.__config, self.filename)
