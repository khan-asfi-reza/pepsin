from pepsin.config import get_project_name


def test_get_project_name():
    name = get_project_name(test="Data")
    assert name == "package"
