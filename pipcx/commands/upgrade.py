"""
Upgrade library module
"""
from argparse import ArgumentParser
from datetime import datetime
from subprocess import CalledProcessError
from typing import List
from urllib import request
from urllib.error import URLError, HTTPError

from pipcx.base import Base
from pipcx.schema import PipcxConfig
from pipcx.utils import pip3_upgrade, update_file, write_file, python_exec


class Command(Base):
    """
    Upgrade module command
    """

    def add_argument(self, parser: ArgumentParser):
        parser.add_argument("libs",
                            nargs="*",
                            help="Libs to be upgraded"
                            )

    @staticmethod
    def handle_upgrade(libs):
        """
        Upgrade or install list of modules
        """
        upgraded = []
        failed = []
        for lib in libs:
            try:
                pip3_upgrade(lib)
                upgraded.append(lib)
            except CalledProcessError:
                failed.append(lib)
        return upgraded, failed

    def execute(self):
        libs: List[str] = self.command_data.get("libs")
        config = PipcxConfig()
        has_pip = False
        if not libs:
            passed, failed = self.handle_upgrade(config.libraries)
        else:
            for lib in libs:
                if 'pip' == lib.split("==")[0]:
                    has_pip = True
                    libs.remove(lib)
                    break
            if has_pip:
                try:
                    with request.urlopen('https://bootstrap.pypa.io/get-pip.py') as file:
                        write_file("get_pip.py", file.read().decode("utf-8"))
                        python_exec("get_pip")
                except (URLError, HTTPError):
                    self.error("Unable to upgrade pip")

            passed, failed = self.handle_upgrade(libs)

        config.update(libraries=passed)
        if failed:
            failed.insert(0, f'# {datetime.now().strftime("%d %B %Y | %H:%M:%S")}')
            update_file("pipcx.failed.log", "\n".join(failed))
