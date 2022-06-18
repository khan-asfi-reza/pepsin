"""
Similar to install
"""
from pipcx.commands.install import Command as InstallCommand


class Command(InstallCommand):
    """
    Install/add command class
    """

    short_description = "Install library"
    help = """Install a particular or multiple libraries
    `$pipcx install <library>`
    Example: `$pipcx install django`
    """
