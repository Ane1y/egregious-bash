import os.path
import sys
from typing import List

from src.Environment import Environment
from src.Executable import BuiltIn


class Cd(BuiltIn):
    """
    Changes current working dir

    Takes 0 or 1 arguments

    When 0 arguments are provided, sets CWD to user's home dir

    When 1 argument is provided, sets CWD to path specified by it
    """

    def impl(self, args: List[str], stdin, stdout):
        if len(args) == 0 or len(args) == 1 and args[0] == '~':
            args = [os.path.expanduser('~')]
        if len(args) != 1:
            print("cd: wrong number of arguments", file=sys.stderr)
            return 1

        new_path = Environment.get_cwd_specific_path(args[0])
        if os.path.isdir(new_path):
            Environment.set_spec_var('cwd', new_path)
        else:
            print(f"cd: dir {new_path} does not exist", file=sys.stderr)
            return 2
        return 0
