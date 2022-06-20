"""
Handles Yaml Config and converts from yaml to dictionary or
dictionary to yaml
"""
import copy
import os
from typing import Any

import yaml


def dict_to_yaml(_dict: dict, filename: str):
    """
    Converts dictionary to yaml
    Args:
        _dict: Python dictionary or hash map
        filename: Name of yaml file
    Returns:

    """
    with open(filename, "w", encoding="utf-8") as file:
        yaml.dump(_dict, file, sort_keys=False)


def yaml_to_dict(filename: str) -> dict:
    """
    Converts yaml  to  dictionary
    Args:
        filename: Name of yaml file

    """
    with open(filename, "r", encoding="utf-8") as file:
        return yaml.load(file, yaml.Loader)


class YAMLConfig:
    """
    Yaml Model controller
    1. Reads yaml file
    2. Saves dictionary to yaml
    3. Reads and stores yaml as dictionary
    4. Appends data to the yaml
    5. Removes data from the yaml
    """

    def __init__(self, filename: str = "temp.yaml", **kwargs):
        self.__config = {}
        self.__filename = ""
        self.__filename = filename
        self.__read_yaml()
        self.append(**kwargs)

    def __read_yaml(self):
        """
        Reads yaml and converts to dictionary and stores it to
        self.__config
        Returns: None
        """
        if os.path.isfile(self.__filename):
            yaml_data = yaml_to_dict(self.__filename)
            self.append(**yaml_data)

    def read_from_yaml(self) -> dict:
        """
        Reads directly from the yaml
        Returns: Yaml Config dictionary
        """
        if os.path.isfile(self.__filename):
            return yaml_to_dict(self.__filename)
        return self.__config

    def append(self, **kwargs):
        """
        Inserts data in the config dictionary
        Returns: None
        """
        self.__config.update(**kwargs)
        for key, val in self.__config.items():
            setattr(self, key, val)

    def remove(self, key) -> Any:
        """
        Removes a given key from the config
        Returns: Any | Removed element from the config
        """
        return self.__config.pop(key)

    def get(self, key) -> Any:
        """
        Returns: Any | Any given element using the key
        """
        return self.__config.setdefault(key, None)

    def get_config(self) -> dict:
        """
        Returns: Dict | returns the copy of the config
        """
        return copy.deepcopy(self.__config)

    def get_filename(self) -> str:
        """
        Returns: str | Yaml Filename
        """
        return self.__filename

    def save(self):
        """
        Saves updated config to the yaml file
        Returns: Dict | self.__config - Yaml config file
        """
        dict_to_yaml(self.__config, self.__filename)
        return self.get_config()
