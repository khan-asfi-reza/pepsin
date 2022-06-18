"""
Uninstall a library
"""
from argparse import ArgumentParser

from pipcx.base import Base
from pipcx.config import PipcxConfig
from pipcx.pyhandler import PyHandler
from pipcx.utils import get_default


class Command(Base):
    """
    Handles library uninstallation
    """

    short_description = "Uninstall library"
    help = """Uninstall a particular or multiple libraries
    `$pipcx uninstall <library>`
    Example: `$pipcx uninstall falcon`
    """

    def add_argument(self, parser: ArgumentParser):
        parser.add_argument(
            "libraries_to_uninstall",
            nargs="+",
            metavar="libs",
            type=str,
            help="Libraries to uninstall",
            default="",
        )

    def execute(self):
        libs = self.command_data.get("libraries_to_uninstall")
        libs = get_default(libs, [])
        if libs:
            config = PipcxConfig()
            py_handler = PyHandler(pipcx_config=config)
            passed = py_handler.uninstall_libraries(libs)[0]
            config.remove_libraries(passed)
