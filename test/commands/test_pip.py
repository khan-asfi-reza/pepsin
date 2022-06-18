import pytest

from pipcx.commands.pip import Command as PipCommand


@pytest.fixture
def pip_command():
    return PipCommand()


def test_pip_command(pip_command):
    pip_command.run(["pipcx", "pip", "help"])
