"""
Upgrade alias
"""
from pepsin.commands.upgrade import Command as UpgradeCommand


class Command(UpgradeCommand):
    """
    Update command / Upgrade Command
    """

    short_description = "Update or upgrade library"
    help = """Upgrades a particular or multiple libraries
        `$pepsin update <library>`
        Example: `$pepsin update django`
        """
