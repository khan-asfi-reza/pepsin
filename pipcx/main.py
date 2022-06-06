import os
import sys

from pipcx.utils import load_command_class, get_commands
from pipcx.version import get_version


class CLI:
    """
    CLI Class that will run the execute command
    """

    def __init__(self):
        self.argv = sys.argv[:]
        self.program_name = os.path.basename(self.argv[0])

        if self.program_name == "__main__.py":
            self.program_name = "python -m pipcx"

        try:
            self.command = self.argv[1]
        except IndexError:
            self.command = "help"

    def get_arg(self, index):
        try:
            return self.argv[index]
        except IndexError:
            return None

    def print_help(self):
        if self.command == 'help':
            string = [
                f"pipcx v{get_version()}",
                "Type the name of the command and --help for help on a specific command",
                "",
                "Available commands: "
            ]
            for command in get_commands():
                command_class = load_command_class(command)
                string.append(
                    f"{command} : {command_class.short_description}"
                )

            return '\n'.join(string)

        elif self.get_arg(2) in ['--help', '-h', 'help']:
            command_class = load_command_class(self.command)
            return command_class.format_help(self.program_name, self.command)

    def execute(self):
        if self.command == 'help':
            sys.stdout.write(self.print_help())
        else:
            command_class = load_command_class(self.command)
            if self.argv[1:] == '--version':
                sys.stdout.write(get_version() + "\n")
            else:
                command_class.run(self.argv)


def main():
    runner = CLI()
    runner.execute()
