"""
Template handling module
"""
import os

from pipcx.const import TEMPLATE_DIR


class TemplateDoesNotExistError(Exception):
    """
    Template Non Existence Error
    """


class Template:
    """
    Template class that is used to save and format Template Files
    """

    def __init__(self, template_name, save_as=None, context=None):
        self.template_name = template_name
        self.file = ""
        self.save_as = template_name if not save_as else save_as
        self.context = {} if not context else context

    def read(self):
        """
        Reads templates file
        """
        temp_name = TEMPLATE_DIR / self.template_name

        if not os.path.isfile(temp_name):
            # Throw if templates does not exist
            raise TemplateDoesNotExistError(f"Template {temp_name} does not exist")

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
        """
        for key, val in self.context.items():
            self.file.replace(f"${key}", val)

    def save(self):
        """
        Saves templates in the working directory
        """
        self.read()
        self.format()
        working_dir = os.getcwd()
        with open(f"{working_dir}/{self.save_as}", "w", encoding="utf-8") as file:
            file.write(self.file)


class TemplateList:
    """
    List of templates that needs to be handled
    """

    def __init__(self):
        self.templates = []

    def add_template(self, *args):
        """
        Adds template in the template queue
        """
        self.templates += args

    def save(self):
        """
        Saves all template
        """
        for template in self.templates:
            template.save()
