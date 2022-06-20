"""
This module handles library Upgrade
"""
from argparse import ArgumentParser

from pepsin.base import Base
from pepsin.config import PepsinConfig
from pepsin.pyhandler import PyHandler
from pepsin.utils import get_default


class Command(Base):
    """
    Upgrade command class
    """

    short_description = "Update or upgrade library"
    help = """Upgrades a particular or multiple libraries
    `$pepsin upgrade <library>`
    Example: `$pepsin upgrade django`
    """

    def add_argument(self, parser: ArgumentParser):
        parser.add_argument(
            "-r",
            type=str,
            metavar="<requirement.txt>",
            help="Upgrade from a text file",
        )

        parser.add_argument(
            "libs",
            nargs="*",
            metavar="<Libraries>",
            type=str,
            help="Libraries to upgrade",
            default="",
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
        libs = get_default(self.command_data.get("libs"), [])
        requirement = self.command_data.get("r")
        if not libs and not requirement:
            libs = config.libraries
        installed = py_handler.upgrade_libraries(
            libs, requirements=requirement
        )[0]
        config.update(libraries=installed)
