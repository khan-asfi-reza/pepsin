"""
Template handling module
"""
import os
from typing import List

from pepsin.const import TEMPLATE_DIR
from pepsin.error import TemplateDoesNotExistError


class Template:
    """
    Template class to save and format Template Files
    """

    def __init__(self, template_name, save_as=None, context=None):
        self.template_name = template_name
        self.file = ""
        self.save_as = template_name if not save_as else save_as
        self.context = {} if not context else context

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

    def save(self):
        """
        Saves templates in the working directory
        Returns:
        """
        self.read()
        self.format()
        working_dir = os.getcwd()
        if not os.path.isfile(os.path.join(working_dir, self.save_as)):
            with open(
                f"{working_dir}/{self.save_as}", "w", encoding="utf-8"
            ) as file:
                file.write(self.file)


class TemplateList:
    """
    Template List DataStructure
    """

    def __init__(self):
        self.templates: List[Template] = []

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
