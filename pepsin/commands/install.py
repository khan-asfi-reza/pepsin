"""
This module handles library installation
"""
from argparse import ArgumentParser

from pepsin.base import Base
from pepsin.config import PepsinConfig
from pepsin.pyhandler import PyHandler
from pepsin.utils import get_default


class Command(Base):
    """
    Install command class
    """

    short_description = "Install library"
    help = """Install a particular or multiple libraries
`$pepsin install <library>`
Example: `$pepsin install django`
"""

    def add_argument(self, parser: ArgumentParser):
        parser.add_argument(
            "libraries_to_install",
            nargs="*",
            metavar="libs",
            type=str,
            help="Libraries to install",
            default="",
        )

        parser.add_argument(
            "-r",
            type=str,
            metavar="requirement.txt",
            help=(
                "Install from a text file, similar to pip install -r"
                " requirements.txt"
            ),
        )

    def execute(self):
        """
        Installs library
        """
        # pepsin Config instance
        config = PepsinConfig()
        # If venv and no config is initialized then create venv and config
        config.initialize_config()
        py_handler = PyHandler(config)
        libs = get_default(self.command_data.get("libraries_to_install"), [])
        requirement = self.command_data.get("r")
        if not libs and not requirement:
            libs = config.libraries
        installed = py_handler.install_libraries(
            libs, requirements=requirement
        )[0]
        config.update(libraries=installed)
