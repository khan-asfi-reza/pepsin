"""
Similar to install
"""
from pepsin.commands.install import Command as InstallCommand


class Command(InstallCommand):
    """
    Install/add command class
    """

    short_description = "Install library"
    help = """Adds/Installs a particular or multiple libraries
    `$pepsin add <library>`
    Example: `$pepsin add django`
    """
