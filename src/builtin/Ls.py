import os
import sys
from typing import List

from src.Environment import Environment
from src.Executable import BuiltIn


class Ls(BuiltIn):
    def impl(self, args: List[str], stdin, stdout):
        if len(args) == 0:
            for file in os.scandir(Environment.get_cwd()):
                print(file.name)
        elif len(args) == 1:
            for file in os.scandir(args[0]):
                print(file.name)
        else:
            print("ls: too many arguments", file=sys.stderr)
            return 1
        return 0
