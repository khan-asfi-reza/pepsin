"""
This module contains Base Class for all commands
"""
import sys
from abc import ABC, abstractmethod
from argparse import ArgumentParser
from typing import Union

from pipcx.error import InvalidCommandError
from pipcx.io import IOBase
from pipcx.version import get_version


class Base(IOBase, ABC):
    """
    The base class which all commands will inherit
    and it contains the signature methods and attributes
    the base class parses the cli arguments,
    converts it into dictionary
    Attributes:
        1. ``help`` is the help text
        that will be shown in the output as help
        for a certain command
        2. ``short_description``
        short possible description to describe a command

    Methods:
        1. ``add_argument`` Adds custom argument to the parser,
        that will be later converted into dictionary
            E.G:
            ```
            def add_argument(self, parser):
                parser.add_argument('--option_1', action='store_true', help='Help Text')
            ```
        2. ``execute`` method is the abstract method that needs to be
        implement in the subclass of Base Class, every
            command must have an ``execute`` method as business logic will be inside this method
    """
    help = ''
    short_description = ''

    def get_parser(self, program_name: str, command: str) -> ArgumentParser:
        """
        Creates Argument Parser Class Object, add 'version' argument
        """
        parser = ArgumentParser(
            prog=f"{program_name} {command}"
        )
        parser.add_argument(
            "--version",
            action="version",
            version=get_version(),
        )
        # Subclass custom arguments will be added via this method
        self.add_argument(parser)
        return parser

    def format_help(self, program_name: str, command: str) -> str:
        """
        returns help text
        """
        return self.get_parser(program_name, command).format_help()

    def add_argument(self, parser: ArgumentParser):
        """
        Subclass custom arguments will be added via this method
        """

    @abstractmethod
    def execute(self, *args, **kwargs) -> Union[None, str]:
        """
        Main logic of the subclass
        """

    def run(self, argv) -> None:
        """
        Runner method for command class
        """
        parser = self.get_parser(program_name=argv[0], command=argv[1])
        options = vars(parser.parse_args(argv[2:]))
        args = options.pop("args", ())
        try:
            self.execute(*args, **options)
        except InvalidCommandError as error:
            self.error(f"{error.__class__.__name__}: {error}")
            sys.exit(error.return_code)
