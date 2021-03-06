import pytest

from pepsin.commands.pip import Pip as PipCommand


@pytest.fixture
def pip_command():
    return PipCommand()


def test_pip_command(pip_command):
    pip_command.run(["pepsin", "pip", "help"])
