"""
Contains Base utility that is required to run the pepsin CLI Class
"""
import enum
import os
from sys import platform


def check_file_exists(file):
    """
    Checks if file exists in working directory
    """
    return os.path.isfile(os.path.join(os.getcwd(), file))


def get_default(target, replace):
    """
    Checks if something is null or empty otherwise return the replacement
    """
    return replace if not target else target


def read_file(file):
    """
    Safely read File and return text
    """
    try:
        with open(file, "r", encoding="utf-8") as __file:
            return __file.read()
    except FileNotFoundError:
        return ""


def write_file(file, text):
    """
    Safely write file
    """
    with open(file, "w", encoding="utf-8") as __file:
        return __file.write(text)


def update_file(file, text):
    """
    Safely updates a file
    """
    read_text = read_file(file)
    write_file(file, read_text + "\n" + text)


def check_dir_exists(*paths):
    """
    Checks if a particular directory exists or not
    Args:
        *paths: Paths to join and check for directory existence

    Returns:

    """
    return os.path.isdir(os.path.join(*paths))


class OSEnum(enum.Enum):
    """
    OS Enum
    """

    LINUX = "linux"
    WIN = "win"
    OSX = "darwin"


def get_os(plt=platform) -> OSEnum:
    """
    Returns System OS Platform name
    """
    __os = OSEnum.LINUX
    if plt in ["linux", "linux2"]:
        __os = OSEnum.LINUX
    elif plt == "darwin":
        __os = OSEnum.OSX
    elif plt in ["win32", "cygwin"]:
        __os = OSEnum.WIN

    return __os
