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
from pipcx.io import PromptHandler, Input
from pipcx.utils import YAMLConfig
from pipcx.utils.spinner import Spinner
from pipcx.utils.venv import install_venv, initialize_venv, activate_venv

MAIN_FILE = """
# Generated with pipcx

if __name__ == "__main__":
   print("Egg and spam")
"""


def initialize_project_config(config: dict, **kwargs):
    """
    Creates base project config file and virtualenv
    """
    venv_dir = kwargs.get("venv", "venv")
    conf_gen = YAMLConfig("pipcx.yaml", **config)
    conf_gen.append(venv=venv_dir)
    conf_gen.save()
    # Installs virtualenv library
    install_venv()
    # Initializes virtualenv
    initialize_venv(venv_dir)
    # Activates virtualenv
    activate_venv(venv_dir)
    # Initialize project file


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
            "project_name",
            nargs='?',
            metavar="project_name",
            type=str,
            help="Name of Project",
            default=''
        )

        parser.add_argument(
            '--venv', help="Virtual Environment directory name"
        )

        parser.add_argument(
            '--no-input', help="Will not take any input", action="store_true"
        )

    def execute(self, *args, **kwargs):
        """
        Inherited execute method
        """
        project_name = kwargs.get("project_name", None)
        spinner = Spinner()
        input_handler = PromptHandler()
        if not project_name:
            input_handler.add_input(
                Input(
                    name="project_name",
                    title="Project Name",
                    default="project",
                    required=False
                )
            )
        input_handler.add_inputs(
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
        config = input_handler.prompt()
        initialize_project_config(config, **kwargs)
        spinner.start()
        # Installs virtualenv library
        project_name = input_handler.answers.project_name
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

        spinner.stop()
        self.output("\nProject initialization complete")
