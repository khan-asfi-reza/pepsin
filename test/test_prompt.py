import pytest

from pepsin.base_io import Input, PromptHandler


@pytest.fixture
def prompt_handler():
    return PromptHandler()


def test_prompt_handler(prompt_handler, monkeypatch):
    """
    Test prompt handler
    """
    prompt_handler.add_prompt(
        Input(name="name", type=str, title="title", required=False)
    )
    assert prompt_handler.__len__() == 1
    # Test 2
    assert not prompt_handler.is_prompt_complete()
    prompt_handler.add_prompts(
        Input(name="title", type=str, title="title", required=False),
        Input(name="age", type=int, title="age", required=False),
    )
    # Test 3
    assert prompt_handler.__len__() == 3
    monkeypatch.setattr("builtins.input", lambda _: "Test")
    prompt_handler.prompt()
    # Test 4
    assert prompt_handler.is_prompt_complete()
    assert prompt_handler.answers.name == "Test"
