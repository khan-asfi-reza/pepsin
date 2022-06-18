"""
Install/Add Alternative
"""
from pipcx.commands.install import Command as InstallCommand


class Command(InstallCommand):
    """
    Install Command alternative
    """

    help = """Install Library using `pipcx i <lib>` """
