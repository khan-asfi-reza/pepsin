"""
Pepsin configuration handler
"""
from datetime import datetime
from typing import Any, Dict, List, Union

from pepsin.utils import check_file_exists, update_file
from pepsin.yml import YAMLConfig


def get_project_name(**options) -> str:
    """
    Returns project name, if project name is
    given use that name otherwise use default name `package`
    Args:
        **options: Dict | CLI arguments and CLI prompt data

    Returns: str | Name of the project

    """
    kw_proj_name: str = options.get("name", None)
    if kw_proj_name:
        return kw_proj_name

    return "package"


def get_or_empty_str(attr: Any) -> Union[Any, str]:
    """
    Mainly for the Pepsin config yaml file,
    PyYaml uses `null` for `None` or `empty` values,
    This function returns empty string if anything is null
    Args:
        attr: Any

    Returns: str | Any
    """
    return "" if not attr else attr


class PepsinConfig:
    """
    Pepsin Config Blueprint and handler
    1. Reads pepsin config / `pepsin.yaml` file
    2. Updates pepsin config
    3. Updates libraries
    4. Removes libraries
    """

    __slots__ = [
        "name",
        "venv",
        "author",
        "license",
        "libraries",
        "scripts",
        "__conf",
    ]

    def __init__(self):
        self.libraries = []
        self.__conf = YAMLConfig("pepsin.yaml")
        self.venv = "venv"
        self.set_config()

    def read_config(self) -> Dict:
        """
        Reads pepsin yaml config and returns dictionary
        Returns: Dict | Reads from yaml file and returns dictionary

        """
        return self.__conf.get_config()

    def set_config(self):
        """
        Sets instance config attributes after reading the
        config file
        Returns: None

        """
        conf = self.read_config()
        for slot in self.get_slots():
            setattr(self, slot, conf.get(slot))
        if not self.libraries:
            self.libraries = []

    def reload(self):
        """
        Reloads config if config has been updated
        Returns:

        """
        self.set_config()

    def get_slots(self):
        """
        Returns: List of slot excluding conf
        """
        return [slot for slot in self.__slots__ if slot != "__conf"]

    @staticmethod
    def config_exists() -> bool:
        """
        Checks if config file exists in the working directory
        Returns: bool
        """
        return check_file_exists("pepsin.yaml")

    def update(self, **kwargs):
        """
        Updates configuration and saves them in the yaml config
        Args:
            **kwargs: Dict | Values to update and save

        Returns:

        """
        libs = kwargs.get("libraries", [])
        # Update libraries
        self.update_libraries(libs)
        for key in kwargs:
            if key != "libraries" and key in self.get_slots():
                setattr(self, key, kwargs.get(key))
        # Update configuration and save to yaml
        self.__conf.append(**self.format_config())
        self.__conf.save()

    def update_libraries(self, libs: List[str]):
        """
        Appends / modified libraries in the config
        If one library already exists in the config, it will pass
        but if the library with different version exists it will be
        replaced with the new one
        Args:
            libs: List[str] | List of libraries

        Returns:

        """
        if not libs:
            return
        for lib in libs:
            # Find similar libraries and remove them
            # 'lib==2.3.4' replace with 'lib=2.3.5'
            # Remove 'lib==2.3.4'
            # Add 'lib==2.3.5'
            # Split using '==' and match first 2 strings
            for conf_lib in self.libraries:
                if lib.split("==")[0] in conf_lib.split("==")[0]:
                    index = self.libraries.index(conf_lib)
                    del self.libraries[index]

            self.libraries.append(lib)

    def remove_libraries(self, libs: List[str]):
        """
        Remove libraries from the config
        Args:
            libs: List[str] List of libraries

        Returns:

        """
        for lib in libs:
            if lib in self.libraries:
                self.libraries.remove(lib)
        # Update configuration and save to yaml
        self.__conf.append(**self.format_config())
        self.__conf.save()

    def format_config(self) -> Dict:
        """
        Formats configuration to dump into yaml file
        Returns: Dict | Dictionary of configurations
        """
        return {
            key: get_or_empty_str(getattr(self, key))
            for key in self.get_slots()
        }

    def initialize_config(self, **kwargs):
        """
        Initialize project configuration if there is no config
        Args:
            kwargs: Additional options
        """
        if not self.config_exists():
            self.update(**kwargs)


def handle_failed_libs(
    failed: List[str], action_msg: str = "Module Installation Failed"
):
    """
    Creates / Updates log file
    Args:
        failed: List[str] List of failed libraries
        action_msg: str | Message to put in the log file

    Returns:

    """
    ftext = (
        f"# {action_msg}" f' {datetime.now().strftime("%d %B %Y | %H:%M:%S")}'
    )
    failed.insert(0, ftext)
    update_file("pepsin.failed.log", "\n".join(failed))
