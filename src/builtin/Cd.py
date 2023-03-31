import os.path
import sys
from typing import List

from src.Environment import Environment
from src.Executable import BuiltIn


class Cd(BuiltIn):
    def impl(self, args: List[str], stdin, stdout):
        if len(args) != 1:
            print("cd: wrong number of arguments", file=sys.stderr)
            return 1
        new_path = os.path.normpath(os.path.join(Environment.get_cwd(), args[0]))
        if os.path.isdir(new_path):
            Environment.set_spec_var('cwd', new_path)
        else:
            print(f"cd: dir {new_path} does not exist", file=sys.stderr)
            return 2
        return 0
