from collections import deque
from test.utils import make_multiple_inputs

import pytest

from pepsin.base_io import Input, IOBase, Output, PromptHandler


@pytest.fixture
def io_base():
    return IOBase()


def test_input_str(monkeypatch):
    """
    Test Input Type String
    """
    monkeypatch.setattr("builtins.input", lambda _: "test")
    string_input = Input(name="name", type=str, title="title")
    assert string_input.prompt_as_dict() == {"name": "test"}


def test_input_int(monkeypatch):
    """
    Test Input Type Integer
    """
    monkeypatch.setattr("builtins.input", lambda _: "1")
    int_input = Input(name="name", type=int, title="title")
    assert int_input.prompt_as_dict() == {"name": 1}


def test_input_boolean(monkeypatch):
    """
    Test Input Type Boolean
    """
    monkeypatch.setattr("builtins.input", lambda _: "y")
    int_input = Input(name="name", type=bool, title="title")
    assert int_input.prompt_as_dict() == {"name": True}


def test_input_options(monkeypatch):
    """
    Test Input Type Options
    """
    monkeypatch.setattr("builtins.input", lambda _: "2")
    int_input = Input(
        name="name", type=int, title="title", options=["option 1", "option 2"]
    )
    assert int_input.prompt_as_dict() == {"name": "option 2"}


def test_input_options_skip(monkeypatch):
    """
    Test Input Type Options
    """
    monkeypatch.setattr(
        "builtins.input",
        make_multiple_inputs(
            [
                "5",
                "1",
            ]
        ),
    )
    int_input = Input(
        name="name", type=int, title="title", options=["option 1", "option 2"]
    )
    assert int_input.prompt_as_dict() == {"name": "option 1"}


def test_input_str_skip(monkeypatch):
    """
    Test input skip while type string
    """
    monkeypatch.setattr("builtins.input", lambda _: "")
    string_input = Input(name="name", type=str, title="title", required=False)
    assert string_input.prompt_as_dict() == {"name": None}


def test_input_bool_skip(monkeypatch):
    """
    Test input skip while type boolean
    """
    monkeypatch.setattr("builtins.input", lambda _: "n")
    string_input = Input(name="name", type=bool, title="title", required=False)
    assert string_input.prompt_as_dict() == {"name": False}


def test_input_default(monkeypatch):
    """
    Test default data
    """
    monkeypatch.setattr("builtins.input", lambda _: "")
    string_input = Input(
        name="name", type=str, default="value", title="title", required=False
    )
    assert string_input.prompt_as_dict() == {"name": "value"}


def test_output(capsys):
    """
    Test output
    """
    output = Output(title="Title", name="Name")
    assert output.prompt_as_dict() == {}
    assert "Title" in capsys.readouterr().out


def test_input_handler(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "test")
    handler = PromptHandler(
        Input(
            name="name",
            type=str,
            default="value",
            title="title",
            required=False,
        )
    )
    handler.prompt()
    assert handler.get("name") == "test"


def test_io_base(io_base):
    io_base.output("Output")
    io_base.error("Error")
    io_base.output_flush()
    io_base.error_flush()
    assert 1
