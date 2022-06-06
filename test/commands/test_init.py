import os
from pathlib import Path
from unittest import TestCase
from pipcx.commands.init import Command as InitCommand
import shutil


class TestInit(TestCase):

    def setUp(self) -> None:
        self.command = InitCommand()
        self.path = Path(__file__).resolve().parent

    def test_command(self):
        os.chdir(path=self.path)
        self.command.run(["pipcx", "init", "--venv=testvenv"])
        self.assertEqual(os.path.isdir("testvenv"), True)

    def tearDown(self) -> None:
        shutil.rmtree(os.path.join(self.path, 'testvenv'))
