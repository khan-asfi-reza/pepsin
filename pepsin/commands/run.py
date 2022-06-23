"""
Runs a script
"""
from argparse import ArgumentParser
from subprocess import CalledProcessError

from pepsin.base import Base
from pepsin.config import PepsinConfig
from pepsin.pyhandler import PyHandler


class Run(Base):
    """
    Handles run script
    """

    short_description = "Runs script"
    help = """Runs a particular or multiple scripts from the config file
    `$pepsin run <script>`
    Example: `$pepsin run start`
    """

    def add_argument(self, parser: ArgumentParser):
        parser.add_argument(
            "script",
            nargs=1,
            metavar="script",
            type=str,
            help="Script to run",
            default="",
        )

        parser.add_argument(
            "command",
            metavar="<command>",
            nargs="*",
            help="Pip command, IE: freeze",
        )

    def execute(self):
        config = PepsinConfig()
        handler = PyHandler(pepsin_config=config)
        script_name = self.command_data.get("script")[0]
        if script_name in config.scripts:
            try:
                handler.python_execute(*config.scripts[script_name].split(" "))
            except CalledProcessError:
                self.error(f"Error in script : {script_name}")
        else:
            self.error(f"No script named {script_name}")
