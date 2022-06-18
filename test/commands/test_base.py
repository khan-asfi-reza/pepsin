from typing import Union

import pytest

from pipcx.base import Base
from pipcx.error import InvalidCommandError


class CommandTest(Base):
    def execute(self, *args, **kwargs) -> Union[None, str]:
        raise InvalidCommandError("Test Error")


@pytest.fixture
def test_base():
    return CommandTest()


def test_format_help(test_base):
    string = test_base.format_help("Test Command", "Test")
    assert "Test Command" in string


def mock_exit(code):
    return


def test_error(test_base, monkeypatch):
    monkeypatch.setattr("sys.exit", mock_exit)
    try:
        test_base.run(argv=["pipcx", "command"])
    except InvalidCommandError as e:
        assert e.return_code == 1
