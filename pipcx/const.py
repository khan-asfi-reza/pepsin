"""
Constant and strings that will be used throughout the project, mainly to easily change the value
"""
from pathlib import Path

COMMAND_NOT_FOUND_ERROR = "use 'pipcx help' to find commands"
PIPCX_ROOT = Path(__file__).resolve().parent
TEMPLATE_DIR = PIPCX_ROOT / "templates"
PIP_DL_LINK = "https://bootstrap.pypa.io/get-pip.py"
