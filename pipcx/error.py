class InvalidCommandError(Exception):
    """
    Exception class indicating a problem while executing a management
    command.
    """

    def __init__(self, return_code=1, *args):
        self.return_code = return_code
        super().__init__(*args)
