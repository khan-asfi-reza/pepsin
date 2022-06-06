from pipcx.base import Base
from pipcx.venv import install_venv, initialize_venv, activate_venv


class Command(Base):
    short_description = "Initialize Virtual environment"

    def execute(self, *args, **kwargs):
        install_venv()
        initialize_venv()
        activate_venv()
