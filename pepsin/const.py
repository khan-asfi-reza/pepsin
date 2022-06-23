"""
Constants that will be used throughout the project
"""
import os
from pathlib import Path

COMMAND_NOT_FOUND_ERROR = "use 'pepsin help' to find commands"
PEPSIN_ROOT = Path(__file__).resolve().parent
TEMPLATE_DIR = PEPSIN_ROOT / "templates"
COMMAND_DIR = os.path.join(PEPSIN_ROOT, "commands")
PIP_DL_LINK = "https://bootstrap.pypa.io/get-pip.py"
