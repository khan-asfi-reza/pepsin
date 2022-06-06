from argparse import ArgumentParser

from pipcx.base import Base
from pipcx.utils.venv import install_venv, initialize_venv, activate_venv


class Command(Base):
    short_description = "Initialize Virtual environment"

    def add_argument(self, parser: ArgumentParser):
        parser.add_argument(
            '--venv', help="Virtual Environment directory name"
        )

    def execute(self, *args, **kwargs):
        venv_dir = kwargs.get("venv", "venv")
        install_venv()
        initialize_venv(venv_dir)
        activate_venv(venv_dir)
