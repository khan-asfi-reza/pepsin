"""
A module for input output handling,
_TODO: Use Rich Library
"""
import abc
import dataclasses
import sys
from collections import namedtuple
from io import TextIOBase
from typing import List, Union

from colorama import Fore, init


class OutputWrapper(TextIOBase):
    """
    Output wrapper that uses std.out and enforces color
    """

    color_map = {
        "success": Fore.GREEN,
        "error": Fore.RED,
        "warning": Fore.YELLOW,
        "primary": Fore.CYAN,
    }

    def __init__(self, out: TextIOBase, ending: str = "\n"):
        super().__init__()
        init(autoreset=True)
        self._out = out
        self.ending = ending

    def flush(self):
        """
        Flush out text
        Returns:

        """
        if hasattr(self._out, "flush"):
            self._out.flush()

    def write(
        self,
        msg: str = "",
        ending: str = None,
        msg_type: str = "text",
        enforce_color: str = "",
    ):
        """
        Outputs text
        Args:
            msg: str | Msg that will be in the output
            ending: str | Ending of the msg
            msg_type: str | Options - success, error, warning, primary
            enforce_color: str | Color of the text

        Returns:

        """
        ending = self.ending if ending is None else ending
        if ending and not msg.endswith(ending):
            msg += ending
        color = self.color_map.get(msg_type, "")
        color = enforce_color if enforce_color else color
        self._out.write(color + msg)


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
    skip: bool = False

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

    color: str = ""

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
        self.output.write(self.title, enforce_color=self.color)


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
        skip: bool | Skips if argument is given
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


class PromptHandler:
    """
    Handles group of input together and stores in the object in
    multiple form
    """

    def __init__(self, *inputs, options=None):
        self.__inputs: List[Input] = []
        self.options = options
        self.add_prompts(*inputs, options=self.options)
        self.__answers = {}

    def update_options(self, options):
        """
        Updates Argument option

        Returns:

        """
        self.options = options

    def __len__(self):
        return len(self.__inputs)

    def is_prompt_complete(self):
        """
        Checks if input has been taken from cli
        """
        return len(self.__answers) > 0

    def add_prompt(self, _input: Input, options=None):
        """
        Add one input in the prompt list, that will be
        executed serially
        _input: `Input` Object
        """
        if not options:
            options = self.options
        if options and options.get(_input.name, None) and _input.skip:
            return
        self.__inputs.append(_input)

    def add_prompts(self, *inputs, options=None):
        """
        Add multiple input in the prompt list, that will be
        executed serially
        inputs: List of `Input` Object
        """
        if not options:
            options = self.options
        self.__inputs += [
            inp
            for inp in inputs
            if not (options and options.get(inp.name, None) and inp.skip)
        ]

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

    def prompt(self, options=None):
        """
        Get input from all the given Input Object
        returns: Dictionary of answers
        """
        for inp in self.__inputs:
            if not (inp.skip and options and options.get(inp.name, None)):
                self.__answers.update(inp.prompt_as_dict())
        return self.__answers

    @property
    def answers(self):
        """
        Returns answer in Class Object Form
        """
        return namedtuple("Answer", self.__answers.keys())(
            *self.__answers.values()
        )
