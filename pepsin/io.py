"""
A module for input output handling,
1. ```OutputWrapper```:
    Handles system standard output, helps to write text
    in the cli and show errors
2. ```IOBase```:
    Is a superclass for Command Classes, that will have
    direct access to the output and error method to show text
    in the cli
3. ```Input```:
    Modified `builtins.input` class to obtain proper modified
    data from the cli
4. ```PromptHandler```:
    Handles multiple `Input` and obtain answers and organizes it
"""
import abc
import dataclasses
import sys
from collections import namedtuple
from io import TextIOBase
from typing import Union


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

    def write(self, msg="", ending=None):
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
class CLIIOBase(abc.ABC):
    """
    CLI Input or output base
    """

    name: str
    title: str

    @abc.abstractmethod
    def prompt(self) -> Union[bool, None, int, str]:
        """
        Read a string from standard input. Then input data
        is fixed and converted to certain data type given by
        `Input.type` or Prints out statement
        """

    @abc.abstractmethod
    def prompt_as_dict(self):
        """
        Returns prompt data dictionary
        """


@dataclasses.dataclass
class Output(IOBase, CLIIOBase):
    """
    Outputs a title while scanning input from the cli
    """

    def __post_init__(self):
        self.output = OutputWrapper(sys.stdout)

    def prompt_as_dict(self):
        """
        Returns empty dictionary
        """
        self.prompt()
        return {}

    def prompt(self):
        """
        Outputs title in the cli
        """
        self.output.write(self.title)


@dataclasses.dataclass
class Input(CLIIOBase):
    """
    params:
        name: str | Name of the input
        title: str | Title that will be displayed in the cli while input prompt
        type: type | Type of input, if options exist then type will be integer for default
        default: Any | Default value of the input
        required: bool | Is the input required or skip-able
        options: list | Available option list
    """

    type: type = str
    default: Union[str, int, bool, None] = None
    required: bool = True
    options: list = dataclasses.field(default_factory=list)

    def __post_init__(self):
        if self.options:
            self.type = int

    def input_title(self) -> str:
        """
        This method returns The prompt string,
        that will be printed along with input
        """
        title = self.title
        if self.type is bool:
            title += " (y/n)"

        if self.options:
            title += "\n"
            for key, option in enumerate(self.options):
                title += f"{key + 1}. {option}\n"

        default = "" if not self.default else self.default

        title += f"[{default}]:"
        return title

    def prompt(self) -> Union[bool, None, int, str]:
        """
        Read a string from standard input. Then input data
        is fixed and converted to certain data type given by
        `Input.type`
        """
        while True:
            title = self.input_title()
            inp = input(title)
            __final = self.default
            __final = inp if inp else __final

            if self.type is int and inp.isdigit():
                data = int(inp)
                if self.options and 0 <= data <= len(self.options):
                    # Option to select and return
                    __final = self.options[data - 1]
                elif not self.options:
                    __final = data
                else:
                    continue

            return inp.lower() in ["1", "y"] if self.type is bool else __final

    def prompt_as_dict(self):
        """
        Returns input in dictionary format
        """
        return {self.name: self.prompt()}


class InputHandler:
    """
    Handles group of input together and stores in the object in
    multiple form
    """

    def __init__(self, *inputs):
        self.__inputs = [*inputs]
        self.__answers = {}

    def __len__(self):
        return len(self.__inputs)

    def is_prompt_complete(self):
        """
        Checks if input has been taken from cli
        """
        return len(self.__answers) > 0

    def add_input(self, _input: Input):
        """
        Add one input in the prompt list, that will be
        executed serially
        _input: `Input` Object
        """
        self.__inputs.append(_input)

    def add_inputs(self, *inputs):
        """
        Add multiple input in the prompt list, that will be
        executed serially
        inputs: List of `Input` Object
        """
        self.__inputs += list(inputs)

    def get_answers(self):
        """
        Returns answers in dict format
        """
        return self.__answers

    def get(self, key):
        """
        Returns one answer using key
        """
        return self.__answers.get(key, None)

    def prompt(self):
        """
        Get input from all the given Input Object
        returns: Dictionary of answers
        """
        for inp in self.__inputs:
            data = inp.prompt_as_dict()
            self.__answers.update(**data)

        return self.__answers

    @property
    def answers(self):
        """
        Returns answer in Class Object Form
        """
        return namedtuple("Answer", self.__answers.keys())(
            *self.__answers.values()
        )
