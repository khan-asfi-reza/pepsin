import os
import shutil


def make_multiple_inputs(inputs: list):
    """ provides a function to call for every input requested. """

    def next_input(_):
        """ provides the first item in the list. """
        return inputs.pop(0)

    return next_input


def safe_remove_dir(dir_path):
    try:
        shutil.rmtree(dir_path)
    except FileNotFoundError:
        pass


def safe_remove_file(file_path):
    try:
        os.remove(file_path)
    except FileNotFoundError:
        pass

