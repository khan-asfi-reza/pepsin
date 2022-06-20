"""
Pepsin Errors
"""


class InvalidCommandError(Exception):
    """
    Exception class indicating a problem while executing a command.
    """

    def __init__(
        self,
        *args,
        return_code=1,
    ):
        self.return_code = return_code
        super().__init__(*args)


class TemplateDoesNotExistError(Exception):
    """
    Template Non Existence Error
    """
