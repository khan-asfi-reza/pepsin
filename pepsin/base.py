"""
Base class for writing commands, commands which will be executed
through the cli
"""
import sys
from abc import ABC, abstractmethod
from argparse import ArgumentParser
from typing import Dict

from pepsin.base_io import IOBase, PromptHandler
from pepsin.error import InvalidCommandError
from pepsin.template import TemplateList
from pepsin.version import get_version


class Base(IOBase, ABC):
    """
    The base class which all commands will inherit
    and it contains the signature methods and attributes

    Attributes:
        1. ``help`` long description of the command
        for a certain command.

        2. ``short_description``
        short possible description to describe a command
        or signify the uses.

        3. ``command_data`` Contains parsed arguments and cli prompt answers
        formatted correctly.

    Methods:
        1. ``add_argument`` Adds custom argument to the parser,
        that will be later converted into dictionary
        Examples
            ```
            def add_argument(self, parser):
                parser.add_argument('--option_1', action='store_true', help='Help Text')
            ```

        2. ``add_prompt`` Adds interactive input and output
        Examples
            ```
            def add_prompt(self, prompt_handler):
                parser.add_prompts(
                    Input(),
                    Output(),
                )
            ```

        3. ``add_template`` Adds templates that will be generated
        after the cli command gets executed
        Examples
            ```
                def add_templates(self, template_list: TemplateList):
                    template_list.add_template(
                        Template(template_name=".gitignore"),
                        Template(
                            template_name="Readme.MD",
                            context={"name": self.command_data.get("name")},
                        ),
                    )
            ```

        4. ``execute`` method is the abstract method
        that needs to be implemented in the subclass, every
        command must have an ``execute`` method
        as business logic will be inside this method
    """

    help = ""
    short_description = ""

    def __init__(self):
        self.prompt_handler: PromptHandler = PromptHandler()
        self.templates: TemplateList = TemplateList()
        self.command_data = {}
        self.command_args = None
        self.argv = []
        super().__init__()

    def add_prompts(self, handler: PromptHandler, **options: Dict):
        """

        Args:
            handler: PromptHandler | PromptHandler Class instance
            **options: Dict | Dictionary containing cli arguments
                       parsed by argparse

        Returns: None

        """

    def add_argument(self, parser: ArgumentParser):
        """
        Subclass method, that will add required arguments
        for the dedicated command
        Args:
            parser: ArgumentParser

        Returns:

        """

    def add_templates(self, template_list: TemplateList):
        """
        Subclass method to add required templates for the dedicated
        command
        Args:
            template_list:

        Returns:

        """

    def format_help(self, command: str) -> str:
        """
        Returns help text
        Args:
            command: str | Name of the command that will be executed

        Returns: str | Formatted help text

        """
        return self.handle_parser(command).format_help()

    def format_arguments(self, **kwargs) -> Dict:
        """
        Formats cli arguments, mainly for the subclass to
        change or edit any options / cli arguments
        Args:
            **kwargs:

        Returns: Dict | Formatted CLI Argument / Options

        """
        return kwargs

    def handle_parser(self, command: str) -> ArgumentParser:
        """
        Creates Argument Parser Class Object, to parse cli arguments
        Args:
            command: str | Name of the command that will be executed

        Returns: ArgumentParser instance

        """
        parser = ArgumentParser(
            prog=f"Pepsin | {command}", description=self.help
        )
        parser.add_argument(
            "--version",
            action="version",
            version=get_version(),
        )
        parser.add_argument("--no-input", action="store_true")
        # Subclass arguments will be added via this method
        self.add_argument(parser)
        return parser

    def handle_input(self, **options):
        """
        This method handles cli inputs, and enquire from the user,
        if the subclass overrides ``add_prompts`` method, containing
        some CLIIoBase Subclass instances, it will call the ``prompt`` method
        of the PromptHandler Instance and take input data from the user and show
        given output
        Args:
            **options: Dict | Dictionary containing cli arguments
                       parsed by argparse

        Returns:

        """
        if options.get("no_input"):
            return
        self.prompt_handler.update_options(options)
        self.add_prompts(self.prompt_handler, **options)
        self.prompt_handler.prompt()

    def handle_template(self):
        """
        Handles subclass added templates
        Returns:

        """
        self.add_templates(self.templates)
        self.templates.save()

    @abstractmethod
    def execute(self):
        """
        Subclass/Command business logic,
        main method where the command's workflow will be declared
        """

    def run(self, argv) -> None:
        """
        Runner method for command class
        """
        # Get the parser to get cli arguments and process
        self.argv = argv[2:]
        parser = self.handle_parser(command=argv[1])
        options = vars(parser.parse_args(argv[2:]))
        args = options.pop("args", ())
        # Handle inputs from the cli
        self.handle_input(**options)
        # Format all inputs
        options.update(**self.prompt_handler.get_answers())
        options = self.format_arguments(**options)
        options.pop("no_input")
        self.command_data = options
        self.command_args = args
        try:
            self.execute()
            self.handle_template()
        except InvalidCommandError as error:
            self.error(f"{error.__class__.__name__}: {error}")
            sys.exit(error.return_code)
