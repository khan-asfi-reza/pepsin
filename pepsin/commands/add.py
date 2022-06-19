"""
Similar to install
"""
from pepsin.commands.install import Command as InstallCommand


class Command(InstallCommand):
    """
    Install/add command class
    """

    short_description = "Install library"
    help = """Install a particular or multiple libraries
    `$pepsin install <library>`
    Example: `$pepsin install django`
    """
