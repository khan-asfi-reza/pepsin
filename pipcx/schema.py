"""
Pipcx config module
"""

from pipcx.utils import YAMLConfig, install_venv, initialize_venv, activate_venv, check_file_exists


def get_project_name(**kwargs):
    """
    Get project name safely
    """
    kw_proj_name = kwargs.get("name", None)
    if kw_proj_name:
        return kw_proj_name

    return "src"


def format_attr(attr):
    """
    Formats attribute and return empty string if Null
    """
    return '' if not attr else attr


def initialize_project_config(**kwargs):
    """
    Creates base project config file and virtualenv
    """
    # Create PipCX Config
    config = PipcxConfig()
    # Generate yaml file 'pipcx.yaml'
    config.update(**kwargs)
    # Installs virtualenv library
    venv_dir = kwargs.get("venv", "venv")
    install_venv()
    # Initializes virtualenv
    initialize_venv(venv_dir)
    # Activates virtualenv
    activate_venv(venv_dir)
    # Initialize project file


class PipcxConfig:
    """
    PIPCX Config blueprint
    """
    __slots__ = ["name",
                 "venv",
                 "author",
                 "license",
                 "libraries",
                 "scripts"]

    conf = YAMLConfig("pipcx.yaml")

    def __init__(self):
        self.libraries = []
        conf = self.conf.get_config()
        for slot in self.__slots__:
            setattr(self, slot, conf.get(slot))

        if not self.libraries:
            self.libraries = []

    @staticmethod
    def config_exists():
        """
        Checks if yaml config exists or not
        """
        return check_file_exists("pipcx.yaml")

    def update(self, **kwargs):
        """
        Update all configuration
        """
        libs = kwargs.get("libraries", [])
        # Update libraries
        self.update_libraries(libs)
        for key in kwargs:
            if key != 'libraries' and key in self.__slots__:
                setattr(self, key, kwargs.get(key))
        # Update configuration and save to yaml
        self.conf.append(**self.format_config())
        self.conf.save()

    def update_libraries(self, libs):
        """
        Update libraries
        """
        if not libs:
            return
        for lib in libs:
            # Find similar libraries and remove them
            # 'lib==2.3.4' replace with 'lib=2.3.5'
            # Remove 'lib==2.3.4'
            # Add 'lib==2.3.5'
            # Split using '==' and match first 2 string
            for conf_lib in self.libraries:
                if lib.split("==")[0] in conf_lib.split("==")[0]:
                    index = self.libraries.index(conf_lib)
                    del self.libraries[index]

            self.libraries.append(lib)

    def format_config(self):
        """
        Return slot configs
        """
        return {key: format_attr(getattr(self, key)) for key in self.__slots__}

    def initialize_config(self, **kwargs):
        """
        Initialize project configuration if there is no config
        """
        if not self.config_exists():
            initialize_project_config(**kwargs)
