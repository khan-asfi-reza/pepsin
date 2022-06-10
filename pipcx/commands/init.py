import os
from argparse import ArgumentParser

from pipcx.base import Base
from pipcx.io import PromptHandler, Input
from pipcx.utils import YamlConfigGenerator
from pipcx.utils.spinner import Spinner
from pipcx.utils.venv import install_venv, initialize_venv, activate_venv

main_file = """
# Generated with pipcx

if __name__ == "__main__":
   print("Egg and spam")
"""


def initialize_project_config(config: dict, **kwargs):
    venv_dir = kwargs.get("venv", "venv")
    conf_gen = YamlConfigGenerator("pipcx.yaml")
    config.update(venv=venv_dir)
    conf_gen.append(**config)
    conf_gen.generate()
    # Installs virtualenv library
    install_venv()
    # Initializes virtualenv
    initialize_venv(venv_dir)
    # Activates virtualenv
    activate_venv(venv_dir)
    # Initialize project file


class Command(Base):
    short_description = "Initialize Virtual environment"

    def add_argument(self, parser: ArgumentParser):
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

    def execute(self, *args, **kwargs):
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

        with open(f"{project_name}/__init__.py", "w"):
            pass

        if not os.path.exists(f"{os.getcwd()}/main.py"):
            with open(f"{project_name}/main.py", "w") as file:
                file.write(main_file)

        spinner.stop()
        self.output("\nProject initialization complete")
