import dataclasses
import sys
from collections import namedtuple
from io import TextIOBase
from typing import Union, List


class OutputWrapper(TextIOBase):
    """
    Wrapper around stdout/stderr
    """

    def __init__(self, out, ending="\n"):
        super().__init__()
        self._out = out
        self.ending = ending

    def flush(self):
        if hasattr(self._out, "flush"):
            self._out.flush()

    def write(self, msg="", style_func=None, ending=None):
        ending = self.ending if ending is None else ending
        if ending and not msg.endswith(ending):
            msg += ending
        self._out.write(msg)


class IOBase:
    """
    IOBase is a superclass for CLI Output and Error Handling
    """

    def __init__(self):
        self.stdout = OutputWrapper(sys.stdout)
        self.stderr = OutputWrapper(sys.stderr)

    def output(self, text):
        """
        Text output on cli
        """
        self.stdout.write(text)

    def output_flush(self):
        """
        Output cli flush
        """
        self.stdout.flush()

    def error(self, text):
        """
        CLI Output for errors
        """
        self.stderr.write(text)

    def error_flush(self):
        """
        CLI Error flush
        """
        self.stderr.flush()


@dataclasses.dataclass
class Input:
    """
    params:
        name: str | Name of the input
        title: str | Title that will be displayed in the cli while input prompt
        type: type | Type of input, if options exist then type will be integer for default
        default: Any | Default value of the input
        required: bool | Is the input required or skip-able
        options: list | Available option list
    """
    name: str
    title: str
    type: type = str
    default: Union[str, int, bool, None] = None
    required: bool = True
    options: list = dataclasses.field(default_factory=list)

    def __post_init__(self):
        if self.options:
            self.type = int

    def input_title(self) -> str:
        """
        Input prompt title
        """
        title = self.title
        if self.type is bool:
            title += " (y/n)"

        if self.options:
            title += '\n'
            for key, option in enumerate(self.options):
                title += f"{key + 1}. {option}\n"

        default = '' if not self.default else self.default

        title += f'[{default}]:'
        return title

    def prompt(self) -> Union[bool, None, int, str]:
        while True:
            title = self.input_title()
            inp = input(title)

            if not self.required and not inp:
                # If the input is required and has default then return default data
                if self.default:
                    return self.default
                # If type is bool then send false else send none
                return False if self.type is bool else None

            if self.type is int and inp.isdigit():
                data = int(inp)
                if self.options and 0 <= data <= len(self.options):
                    # Option to select and return
                    return self.options[data - 1]
                elif not self.options:
                    return data
                else:
                    continue

            if self.type is bool:
                if inp.lower() in ['1', 'y']:
                    return True
                else:
                    return False

            if inp:
                return inp

    def prompt_as_dict(self):
        return {self.name: self.prompt()}


class PromptHandler:
    __inputs: List[Input] = []
    __answers = {}

    def __init__(self, *inputs):
        self.__inputs = [*inputs]

    def __len__(self):
        return len(self.__inputs)

    def is_prompt_complete(self):
        return len(self.__answers) > 0

    def add_input(self, _input: Input):
        self.__inputs.append(_input)

    def add_inputs(self, *inputs):
        self.__inputs += list(inputs)

    def prompt(self):
        for inp in self.__inputs:
            self.__answers.update(**inp.prompt_as_dict())

        return self.__answers

    @property
    def answers(self):
        return namedtuple("Answer", self.__answers.keys())(*self.__answers.values())
