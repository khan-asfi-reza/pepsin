"""
Install/Add Alternative
"""
from pepsin.commands.install import Command as InstallCommand


class Command(InstallCommand):
    """
    Install Command alternative
    """

    help = """Install Library using `pepsin i <lib>` """
