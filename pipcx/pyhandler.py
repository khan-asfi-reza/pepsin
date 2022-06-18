"""
This module handles python and pip execution
"""
import os
import subprocess
import sys
from typing import List
from urllib import request
from urllib.error import HTTPError, URLError

from pipcx.config import PipcxConfig, handle_failed_libs
from pipcx.const import PIP_DL_LINK
from pipcx.io import OutputWrapper
from pipcx.utils import (
    OSEnum,
    check_dir_exists,
    check_file_exists,
    get_default,
    get_os,
    read_file,
    write_file,
)


class PyHandler:
    """
    Handles python and pip package installation, management
    """

    def __init__(
        self, pipcx_config=None, stdout=None, stderr=None, skip_venv=False
    ):
        """
        Save env variable and set env variable to run code
        Using venv
        Args:
            pipcx_config: PipcxConfig Instance
            stdout: OutputWrapper(sys.stdout) Instance
            stderr: OutputWrapper(sys.stderr) Instance
            skip_venv: Skip initializing venv on init
        """
        # Read pipcx config to get venv
        self.output = stdout if stdout else OutputWrapper(sys.stdout)
        self.error = stderr if stderr else OutputWrapper(sys.stderr)
        self.executable = "python" if get_os() == OSEnum.WIN else "python3"
        self.pip_exec = "pip" if get_os() == OSEnum.WIN else "pip3"
        self.pipcx_config = pipcx_config if pipcx_config else PipcxConfig()
        self.env = os.environ.copy()

        self.venv = self.pipcx_config.venv
        # Create virtualenv if not exist
        if not (skip_venv and not self.venv) or (
            self.venv and not check_dir_exists(os.getcwd(), self.venv)
        ):
            self.venv = get_default(self.venv, "venv")
            self.pipcx_config.update(venv=self.venv)
            self.init_venv(self.venv)

        self.set_env()

    @staticmethod
    def __join_env_path(script_dir):
        """
        Joins script path and Returns ENV Path
        Args:
            script_dir: Venv Script Path

        Returns: string
        """
        return os.pathsep.join(
            [script_dir] + os.environ.get("PATH", "").split(os.pathsep)
        )

    def set_env(self):
        """
        Sets up environment variable

        Returns: None
        """
        if self.venv:
            sys_os = get_os()
            script_loc = "bin"
            if sys_os == OSEnum.WIN:
                script_loc = "scripts"
            venv_dir = os.path.join(os.getcwd(), self.venv)
            script_dir = os.path.join(os.getcwd(), self.venv, script_loc)
            self.env["VIRTUAL_ENV"] = venv_dir
            self.env["PATH"] = self.__join_env_path(script_dir)
            self.executable = f"{script_dir}/python"
            self.pip_exec = f"{script_dir}/pip"

    def python_execute(self, *commands):
        """
        Executes python command
        """
        subprocess.check_call([self.executable, *commands], env=self.env)

    def init_venv(self, venv_dir):
        """
        Initializes virtualenv directory
        """
        self.python_execute("-m", "virtualenv", venv_dir)

    def pip_execute(self, *commands):
        """
        Executes pip command
        """
        subprocess.check_call([self.pip_exec, *commands], env=self.env)

    def pip_install(self, *packages):
        """
        Installs packages through pip
        """
        subprocess.check_call(
            [self.pip_exec, "install", *packages], env=self.env
        )

    def pip_upgrade(self, *packages):
        """
        Upgrades pip package
        """
        package_list = list(packages)
        # This part of the code safely upgrades pip
        # Default upgrade can cause unusual pip behaviors
        has_pip = False
        if "pip" in package_list or "pip3" in package_list:
            has_pip = True
            to_remove = "pip3" if "pip3" in package_list else "pip"
            package_list.remove(to_remove)
        if has_pip:
            try:
                with request.urlopen(PIP_DL_LINK) as file:
                    write_file("get_pip.py", file.read().decode("utf-8"))
                    self.python_execute("get_pip")
            except (URLError, HTTPError):
                self.error.write("Unable to upgrade pip")
        subprocess.check_call(
            [self.pip_exec, "install", "--upgrade", *package_list],
            shell=True,
            env=self.env,
        )

    def __process_library(
        self, action, libs=None, requirements=""
    ) -> (List[str], List[str]):
        """
        Process library with action
        Args:
            action: Option["install" , "upgrade"]
            libs: List of libraries
            requirements: Requirement.txt or text requirement file
        Returns:
            Tuple: List of passed and failed libraries

        """
        passed = []
        failed = []
        to_install: List[str] = get_default(libs, [])
        if requirements:
            if not check_file_exists(requirements):
                self.error.write(f"{requirements} does not exist")
            else:
                to_install += read_file(requirements).split("\n")
                to_install = [each for each in to_install if "#" not in each]
        for lib in to_install:
            try:
                if action == "upgrade":
                    self.pip_upgrade(lib)
                else:
                    self.pip_install(lib)
                if lib not in ["pip", "pip3"]:
                    passed.append(lib)
            except subprocess.CalledProcessError:
                self.error.write(f"Unable to install {lib}")
                failed.append(lib)

        if failed:
            handle_failed_libs(failed)

        return passed, failed

    def install_libraries(
        self, libs=None, requirements=""
    ) -> (List[str], List[str]):
        """
        Installs multiple libraries
        Args:
            libs: List of libraries
            requirements : Requirement.txt or text requirement file
        Returns:
            tuple: List of passed and failed libraries
        """
        return self.__process_library("install", libs, requirements)

    def upgrade_libraries(self, libs=None, requirements=""):
        """
        Upgrades multiple libraries
        Args:
            libs: List of libraries
            requirements : Requirement.txt or text requirement file
        Returns:
            tuple: List of passed and failed libraries
        """
        return self.__process_library("upgrade", libs, requirements)
