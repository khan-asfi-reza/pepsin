import pytest

from pipcx.io import Input, IOBase


def test_input_str(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: 'test')
    string_input = Input(name="name", type=str, title="title")
    assert string_input.prompt_as_dict() == {'name': 'test'}


def test_input_int(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: '1')
    int_input = Input(name="name", type=int, title="title")
    assert int_input.prompt_as_dict() == {'name': 1}


def test_input_boolean(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: 'y')
    int_input = Input(name="name", type=bool, title="title")
    assert int_input.prompt_as_dict() == {'name': True}


def test_input_options(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: '2')
    int_input = Input(name="name", type=int, title="title", options=['option 1', 'option 2'])
    assert int_input.prompt_as_dict() == {'name': 'option 2'}


def test_input_str_skip(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: '')
    string_input = Input(name="name", type=str, title="title", required=False)
    assert string_input.prompt_as_dict() == {'name': None}


def test_input_bool_skip(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: '')
    string_input = Input(name="name", type=bool, title="title", required=False)
    assert string_input.prompt_as_dict() == {'name': False}


def test_input_default(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: '')
    string_input = Input(name="name", type=str, default='value', title="title", required=False)
    assert string_input.prompt_as_dict() == {'name': 'value'}


@pytest.fixture
def io_base():
    return IOBase()


def test_io_base(io_base):
    io_base.output("Output")
    io_base.error("Error")
    io_base.output_flush()
    io_base.error_flush()
    assert 1