"""
Handles Yaml Config and converts from yaml to dictionary or
dictionary to yaml
"""
import copy
import os

import yaml


def dict_to_yaml(_dict, filename):
    """
    Converts dictionary to yaml
    _dict: Python dictionary or hash map
    filename: Name of yaml file
    """
    with open(filename, "w", encoding="utf-8") as file:
        yaml.dump(_dict, file, sort_keys=False)


def yaml_to_dict(filename) -> dict:
    """
    Converts yaml  to  dictionary
    filename: Name of yaml file
    """
    with open(filename, "r", encoding="utf-8") as file:
        return yaml.load(file, yaml.Loader)


class YAMLConfig:
    """
    Yaml Model controller
    """

    def __init__(self, filename="temp.yaml", **kwargs):
        self.__config = {}
        self.__filename = ""
        self.__filename = filename
        self.__read_yaml()
        self.append(**kwargs)

    def __read_yaml(self):
        """
        Reads yaml file
        """
        if os.path.isfile(self.__filename):
            yaml_data = yaml_to_dict(self.__filename)
            self.append(**yaml_data)

    def read_from_yaml(self):
        """
        Reads directly from yaml file
        """
        if os.path.isfile(self.__filename):
            return yaml_to_dict(self.__filename)
        return self.__config

    def append(self, **kwargs):
        """
        Inserts config data in the config dictionary
        """
        self.__config.update(**kwargs)
        for key, val in self.__config.items():
            setattr(self, key, val)

    def remove(self, key):
        """
        Removes data from config
        """
        return self.__config.pop(key)

    def get(self, key):
        """
        Gets config using key
        """
        return self.__config.get(key, None)

    def get_config(self):
        """
        Returns the config
        """
        return copy.deepcopy(self.__config)

    def get_filename(self):
        """
        Returns the filename
        """
        return self.__filename

    def save(self):
        """
        Saves config in the yaml file
        """
        dict_to_yaml(self.__config, self.__filename)
        return self.__config
