"""
Init Command
Usage:
    `pepsin init`

Generates a python project along
with virtual environment.

`init` will prompt for 6 things such as
1. Project Name
2. Project description
3. Github repo
4. License
5. Author
6. Email

and will create a project folder under the name
`project_name`

Optional Parameters:

`pepsin init my_project`
Will create project without asking for project_name

`--venv=myVenv`
Custom venv directory

`--no-input`
Will ignore the prompt part
"""
from argparse import ArgumentParser

from colorama import Fore

from pepsin.base import BaseCommand
from pepsin.base_io import Input, Output
from pepsin.config import PepsinConfig, get_project_name
from pepsin.pyhandler import PyHandler
from pepsin.template import (
    Template,
    TemplateDirectory,
    TemplateFromString,
    TemplateList,
)


class Init(BaseCommand):
    """
    Init command class
    """

    short_description = "Initialize Virtual environment"
    help = """Initialize virtual environment, project data and file
    """

    def add_argument(self, parser: ArgumentParser):
        """
        Adds custom argument
        """
        parser.add_argument(
            "name",
            nargs="?",
            metavar="name",
            type=str,
            help="Name of Project",
            default="",
        )

        parser.add_argument(
            "--venv", help="Virtual Environment directory name", default="venv"
        )

    def add_prompts(self, handler, **options):
        """
        Handles prompt input
        """
        handler.add_prompts(
            Output(
                name="Welcome",
                title=f"Pepsin Setup Project\n{'-' * 10}",
                color=Fore.CYAN,
            ),
            Input(
                name="name",
                title="Project Name",
                default="src",
                required=False,
                skip=True,
            ),
            Input(
                name="description",
                title="Description",
                default="",
                required=False,
                skip=True,
            ),
            Input(
                name="github",
                title="Github Repo",
                default="",
                required=False,
                skip=True,
            ),
            Input(
                name="author", title="Author", default="Author", required=False
            ),
            Input(
                name="email",
                title="Email",
                default="email@email.com",
                required=False,
            ),
            Input(
                name="license", title="license", default="MIT", required=False
            ),
        )

    def format_arguments(self, **kwargs):
        """
        Formats command arguments and input
        """
        project_name = get_project_name(**kwargs)
        kwargs.update(name=project_name)
        return kwargs

    def add_templates(self, template_list: TemplateList):
        """
        Adds custom template
        """
        project_name = self.command_data.get("name")
        template_list.add_template(
            # Base Directory / Project Directory
            TemplateDirectory(
                project_name,
            ),
            # Project Base Python File
            TemplateFromString("__init__.py", text="", directory=project_name),
            Template(
                "main.py",
                directory=project_name,
            ),
            # Project Test File
            Template(
                "template_test.py",
                directory=f"{project_name}/tests",
                save_as="test_package.py",
            ),
            # Config files
            Template(template_name=".gitignore"),
            Template(
                template_name="Readme.MD",
                context={"name": self.command_data.get("name")},
            ),
        )

    def execute(self):
        """
        Inherited execute method
        """
        conf = PepsinConfig()
        conf.update(
            self.command_data,
            scripts={"main": f"{self.command_data.get('name')}/main.py"},
        )
        PyHandler(conf, self.stdout, self.stderr)
        # Installs virtualenv library
        self.output("\nProject initialization complete")
