"""
This module handles library installation
"""
from datetime import datetime
from argparse import ArgumentParser
from subprocess import CalledProcessError

from pipcx.base import Base
from pipcx.schema import PipcxConfig
from pipcx.utils import pip3_install, check_file_exists, get_default, read_file, update_file


class Command(Base):
    """
    Install command class
    """
    def add_argument(self, parser: ArgumentParser):
        parser.add_argument(
            '-r',
            type=str,
            metavar="requirement.txt",
            help="Install from a text file"
        )

        parser.add_argument(
            "libs",
            nargs='*',
            metavar="libs",
            type=str,
            help="Libraries to install",
            default='',
        )

    def execute(self):
        """
        Installs library
        """
        # Pipcx Config instance
        config = PipcxConfig()
        # If venv and no config is initialized then create venv and config
        config.initialize_config()
        installed_libraries = []
        failed = []
        libs = get_default(self.command_data.get("libs"), [])
        requirement_file = self.command_data.get("r")
        if requirement_file:
            if not check_file_exists(requirement_file):
                self.error(f"{requirement_file} does not exist in working directory")
            else:
                libs += read_file(requirement_file).split("\n")
        for lib in libs:
            try:
                pip3_install(lib)
                installed_libraries.append(lib)
            except CalledProcessError:
                failed.append(lib)
        config.update(libraries=installed_libraries)

        if failed:
            failed.insert(0, f'# {datetime.now().strftime("%d %B %Y | %H:%M:%S")}')
            update_file("pipcx.failed.log", "\n".join(failed))
