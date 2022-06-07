from argparse import ArgumentParser

from pipcx.base import Base
from pipcx.error import InvalidCommandError
from pipcx.utils.venv import install_venv, initialize_venv, activate_venv


class Command(Base):
    short_description = "Initialize Virtual environment"

    def add_argument(self, parser: ArgumentParser):
        parser.add_argument(
            "virtualenv",
            nargs='?',
            metavar="virtualenv",
            type=str,
            help="Name of virtualenv directory",
            default=''

        )

        parser.add_argument(
            '--venv', help="Virtual Environment directory name"
        )

    def execute(self, *args, **kwargs):
        venv_dir = kwargs.get("venv", None)
        virtual_env = kwargs.get("virtualenv", None)

        # Only one argument is allowed
        if virtual_env and venv_dir:
            raise InvalidCommandError("2 Virtualenv directory name provided, "
                                      "use either pipcx init 'name' or pipcx init --venv='name'")

        elif virtual_env and not venv_dir:
            name = virtual_env

        elif venv_dir and not virtual_env:
            name = venv_dir

        else:
            name = 'venv'
        # Installs virtualenv library
        install_venv()
        # Initializes virtualenv
        initialize_venv(name)
        # Activates virtualenv
        activate_venv(name)
