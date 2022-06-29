"""
Template handling module
"""
import os
from abc import ABC, abstractmethod
from pathlib import Path
from typing import List

from pepsin.const import TEMPLATE_DIR
from pepsin.error import TemplateDoesNotExistError
from pepsin.utils import check_dir_exists, write_file


class BaseTemplate(ABC):
    def __init__(self):
        self.directory = os.getcwd()

    @abstractmethod
    def handle(self):
        """
        Saves templates in the working directory
        Returns:
        """

    def save(self):
        """
        Calls the save method of the child class
        and creates directory safely
        Returns:
        """
        if not check_dir_exists(self.directory):
            Path(self.directory).mkdir(parents=True, exist_ok=True)
        self.handle()


class Template(BaseTemplate):
    """
    Template class to save and format Template Files
    """

    def __init__(
        self, template_name="", directory="", save_as=None, context=None
    ):
        """

        Args:
            template_name: Name of the template stored in the templates directory
            directory: Given directory, where to store the file
            save_as: Name of the file that will be saved, default as template name
            context: Data to fill in the template
        """
        super().__init__()
        self.template_name = template_name
        self.file = ""
        self.save_as = template_name if not save_as else save_as
        self.context = {} if not context else context
        self.directory = f"{os.getcwd()}/{directory}"

    def read(self):
        """
        Reads a given template file and saves template file data
        to self.file
        Returns:

        """
        temp_name = TEMPLATE_DIR / self.template_name

        if not os.path.isfile(temp_name):
            # Throw if templates does not exist
            raise TemplateDoesNotExistError(
                f"Template {temp_name} does not exist"
            )

        with open(temp_name, "r", encoding="utf-8") as file:
            self.file = file.read()

    def format(self):
        """
        Reads the file, stores data in the file attribute
        Then exchanges the context data, that starts with `$`
        For example in a templates file a context variable named
        `file`, in the templates that must be written as following
        `$file`
        While initializing `Template` class along with context parameter
        Template("templates.py", context={"file": "FooFile"})
        'save' method will save the file where $file will be replaced with FooFile

        Returns:

        """
        for key, val in self.context.items():
            self.file.replace(f"${key}", val)

    def handle(self):
        """
        Saves templates in the working directory
        Returns:
        """
        self.read()
        self.format()
        if not os.path.isfile(os.path.join(self.directory, self.save_as)):
            write_file(f"{self.directory}/{self.save_as}", self.file)


class TemplateDirectory(BaseTemplate):
    """
    Handles only directory creation
    """

    def __init__(self, name):
        """
        Creates nested directory
        Args:
            name: name of the directory
        """
        super().__init__()
        self.directory = f"{os.getcwd()}/{name}"

    def handle(self):
        """
        Creates directory via the parent run_save method
        Returns:

        """


class TemplateFromString(BaseTemplate):
    """
    Creates file in the given directory without a given template
    and from text string
    """

    def __init__(self, name, text, directory=""):
        """

        Args:
            name: Name of the file
            text: Text to be in the file
            directory: Directory where to store the file
        """
        super().__init__()
        self.directory = f"{os.getcwd()}/{directory}"
        self.name = name
        self.text = text

    def handle(self):
        write_file(f"{self.directory}/{self.name}", self.text)


class TemplateList:
    """
    Template List DataStructure,
    to handle all the given Templates
    """

    def __init__(self):
        self.templates: List[BaseTemplate] = []

    def add_template(self, *args):
        """
        Adds templates in the queue
        Args:
            *args: List[Templates] list of templates

        Returns:

        """
        self.templates += args

    def save(self):
        """
        Executes the template.save() method for
        all the given templates
        Returns:

        """
        for template in self.templates:
            template.save()
