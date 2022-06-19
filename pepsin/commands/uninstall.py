"""
Uninstall a library
"""
from argparse import ArgumentParser

from pepsin.base import Base
from pepsin.config import PepsinConfig
from pepsin.pyhandler import PyHandler
from pepsin.utils import get_default


class Command(Base):
    """
    Handles library uninstallation
    """

    short_description = "Uninstall library"
    help = """Uninstall a particular or multiple libraries
    `$pepsin uninstall <library>`
    Example: `$pepsin uninstall falcon`
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
            config = PepsinConfig()
            py_handler = PyHandler(pepsin_config=config)
            passed = py_handler.uninstall_libraries(libs)[0]
            config.remove_libraries(passed)
