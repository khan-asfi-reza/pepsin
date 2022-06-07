import dataclasses
import sys
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

    def write(self, msg="", style_func=None, ending=None):
        ending = self.ending if ending is None else ending
        if ending and not msg.endswith(ending):
            msg += ending
        self._out.write(msg)


class IOBase:
    def __init__(self):
        self.stdout = OutputWrapper(sys.stdout)
        self.stderr = OutputWrapper(sys.stderr)

    def output(self, text):
        self.stdout.write(text)

    def output_flush(self):
        self.stdout.flush()

    def error(self, text):
        self.stderr.write(text)

    def error_flush(self):
        self.stderr.flush()


@dataclasses.dataclass
class Input:
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
                if self.default:
                    return self.default
                return False if self.type is bool else None

            if self.type is int and inp.isdigit():
                data = int(inp)
                if self.options and 0 <= data <= len(self.options):
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
