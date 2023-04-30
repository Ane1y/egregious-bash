import os
import sys
from typing import List

from src.Environment import Environment
from src.Executable import BuiltIn


class Ls(BuiltIn):
    """
    Prints contents of the directory

    Takes 0 or 1 arguments

    When 0 arguments are provided, prints contents of CWD

    When 1 argument is provided, prints contents of the folder specified by it
    """
    def impl(self, args: List[str], stdin, stdout):
        if len(args) == 0:
            for file in os.scandir(Environment.get_cwd()):
                print(file.name)
            return 0

        if len(args) != 1:
            print("ls: too many arguments", file=sys.stderr)
            return 1

        path = Environment.get_cwd_specific_path(args[0])
        if os.path.isdir(path):
            for file in os.scandir(path):
                print(file.name)
        else:
            print(f"ls: \"{path}\" is not a folder", file=sys.stderr)
            return 1

        return 0
