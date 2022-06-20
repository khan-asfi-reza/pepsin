"""
Install/Add Alternative
"""
from pepsin.commands.install import Command as InstallCommand


class Command(InstallCommand):
    """
    Install Command alternative
    """

    short_description = "Installs library"
    help = """Install a particular or multiple libraries
        `$pepsin i <library>`
        Example: `$pepsin i django`
        """
