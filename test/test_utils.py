from pipcx.utils import get_default, read_file, write_file, update_file, check_file_exists
from test.utils import temp_path, safe_remove_file


def test_get_default(temp_path):
    test_data = None
    data = get_default(test_data, "test")
    assert data == "test"


def test_read_file(temp_path):
    read = read_file("test.txt")
    assert read == ""


def test_update_file(temp_path):
    write_file("test_write.txt", "test")
    update_file("test_write.txt", "update")
    read = read_file("test_write.txt")
    assert "test" in read
    assert "update" in read
    safe_remove_file("test_write.txt")


def test_check_file_exists():
    assert not check_file_exists("dummy.txt")
