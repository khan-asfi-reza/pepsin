"""
This module contains Base Class for all commands
"""
import sys
from abc import ABC, abstractmethod
from argparse import ArgumentParser

from pipcx.error import InvalidCommandError
from pipcx.io import InputHandler, IOBase
from pipcx.template import TemplateList
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

    help = ""
    short_description = ""

    def __init__(self):
        self.input_handler: InputHandler = InputHandler()
        self.templates: TemplateList = TemplateList()
        self.command_data = {}
        self.command_args = None
        self.argv = []
        super().__init__()

    def add_input(self, handler, **options):
        """
        Adds input - Superclass
        """

    def handle_input(self, **options):
        """
        Input handler function
        """
        if options.get("no_input"):
            return

        self.add_input(self.input_handler, **options)
        self.input_handler.prompt()

    def get_parser(self, program_name: str, command: str) -> ArgumentParser:
        """
        Creates Argument Parser Class Object, add 'version' argument
        """
        parser = ArgumentParser(prog=f"{program_name} {command}")
        parser.add_argument(
            "--version",
            action="version",
            version=get_version(),
        )
        parser.add_argument("--no-input", action="store_true")
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

    def format_arguments(self, **kwargs):
        """
        Format Arguments
        """
        return kwargs

    def add_templates(self, template_list):
        """
        Subclass templates will be added
        """

    def handle_template(self):
        """
        Handles all template
        """
        self.add_templates(self.templates)
        self.templates.save()

    @abstractmethod
    def execute(self):
        """
        Main logic of the subclass
        """

    def run(self, argv) -> None:
        """
        Runner method for command class
        """
        # Get the parser to get cli arguments and process
        self.argv = argv[2:]
        parser = self.get_parser(program_name=argv[0], command=argv[1])
        data = vars(parser.parse_args(argv[2:]))
        args = data.pop("args", ())
        # Handle inputs from the cli
        self.handle_input(**data)
        # Format all inputs
        data.update(**self.input_handler.get_answers())
        data = self.format_arguments(**data)
        data.pop("no_input")
        self.command_data = data
        self.command_args = args
        try:
            self.execute()
            self.handle_template()
        except InvalidCommandError as error:
            self.error(f"{error.__class__.__name__}: {error}")
            sys.exit(error.return_code)
