"""
Install Command
Usage:
    `pepsin install <library>`

Installs libraries and store library name in the config file

``
$pepsin install django flask
``

Optional Parameters:
`-r=requirement.txt`
Requirement file containing library names

"""
from argparse import ArgumentParser

from pepsin.base import BaseCommand
from pepsin.config import PepsinConfig
from pepsin.pyhandler import PyHandler
from pepsin.utils import get_default


class Install(BaseCommand):
    """
    Install command class
    """

    short_description = "Install library"
    help = """Install a particular or multiple libraries
`$pepsin install <library>`
Example: `$pepsin install django`
"""
    alias = ["i", "add", "append"]

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
