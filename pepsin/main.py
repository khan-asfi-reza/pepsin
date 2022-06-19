"""
Main File where the main function and CLI Class is executed and defined
"""
import os
import sys

from pepsin.base_io import IOBase
from pepsin.const import COMMAND_NOT_FOUND_ERROR
from pepsin.utils.base import get_commands, load_command_class
from pepsin.version import get_version


class CLI(IOBase):
    """
    CLI Class that will run the execute command
    """

    def __init__(self, argv=None):
        super().__init__()
        self.argv = sys.argv[:] if not argv else argv
        self.program_name = os.path.basename(self.argv[0])

        if self.program_name == "__main__.py":
            self.program_name = "python -m pepsin"

        try:
            self.command = self.argv[1]
        except IndexError:
            self.command = "help"

    def get_arg(self, index):
        """
        index: System Argument List index
        Returns System Argument safely and IndexError is handled
        """
        try:
            return self.argv[index]
        except IndexError:
            return None

    def print_help(self) -> str:
        """
        Returns Help Text
        """
        version = get_version()
        if self.command in ["--help", "-h", "help"]:
            string = [
                f"pepsin v{version}",
                "Type the name of the command and --help for help on a"
                " specific command",
                "",
                "Available commands: ",
            ]
            for command in get_commands():
                command_class = load_command_class(command)
                string.append(f"{command} | {command_class.short_description}")

            return "\n".join(string)

        command_class = load_command_class(self.command)
        return command_class.format_help(self.command)

    def execute(self):
        """
        Executes the commands or throws error or prints help text
        """
        if self.command in ["--help", "-h", "help"]:
            help_text = self.print_help()
            self.output(help_text)

        elif self.command == "--version" or self.argv[1:] == "--version":
            version = get_version()
            self.output(version + "\n")

        else:
            try:
                command_class = load_command_class(self.command)
                command_class.run(self.argv)
            except ModuleNotFoundError:
                self.error(f"`{self.command}` Command not available")
                self.error(COMMAND_NOT_FOUND_ERROR)


def main():
    """
    Main code runner function
    """
    runner = CLI()
    runner.execute()
