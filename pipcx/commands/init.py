"""
Init Command
Usage:
    `pipcx init`

Generates a python boilerplate normal project along
with virtual environment.

`init` will prompt for 4 things such as
1. project_name
2. License
3. Author
4. Email

and will create a project folder under the name
`project_name`

Optional Parameters:

`pipcx init my_project`
Will create project without asking for project_name

`--venv=myVenv`
Custom venv directory

`--no-input`
Will not take any input
"""
import os
from argparse import ArgumentParser

from pipcx.base import Base
from pipcx.io import Input
from pipcx.schema import get_project_name, initialize_project_config

MAIN_FILE = ""
"""# Generated with pipcx

if __name__ == "__main__":
    print("Egg and spam")
"""


class Command(Base):
    """
    Init command class
    """

    short_description = "Initialize Virtual environment"

    def add_argument(self, parser: ArgumentParser):
        """
        Adds custom argument
        """
        parser.add_argument(
            "name",
            nargs='?',
            metavar="name",
            type=str,
            help="Name of Project",
            default=''
        )

        parser.add_argument(
            '--venv', help="Virtual Environment directory name", default="venv"
        )

    def add_input(self, handler, **options):
        """
        Handles prompt input
        """
        project_name = options.get("name", None)

        if not project_name:
            handler.add_input(
                Input(
                    name="name",
                    title="Project Name",
                    default="src",
                    required=False
                )
            )

        handler.add_inputs(
            Input(
                name="author",
                title="Author",
                default="Author",
                required=False
            ),
            Input(
                name="email",
                title="Email",
                default="email@email.com",
                required=False
            ),
            Input(
                name="license",
                title="license",
                default="MIT",
                required=False
            ),
        )

    def format_arguments(self, **kwargs):
        """
        Formats command arguments and input
        """
        project_name = get_project_name(**kwargs)
        kwargs.update(name=project_name)
        return kwargs

    @staticmethod
    def handle_directory(**kwargs):
        """
        Handle directory creation
        """
        project_name = kwargs.get("name")
        try:
            os.mkdir(project_name)
        except FileExistsError:
            pass

        with open(f"{project_name}/__init__.py", "w", encoding="utf-8"):
            pass
        working_dir = os.getcwd()

        if not os.path.exists(f"{working_dir}/{project_name}/main.py"):
            with open(f"{project_name}/main.py", "w", encoding="utf-8") as file:
                file.write(MAIN_FILE)

    def execute(self, **command_data):
        """
        Inherited execute method
        """
        initialize_project_config(**command_data)
        # Installs virtualenv library
        self.handle_directory(**command_data)
        self.output("\nProject initialization complete")
