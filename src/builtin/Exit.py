import sys
from typing import List
from Executable import BuiltIn


class Exit(BuiltIn):
    def exec(self, args: List[str]):
        sys.exit(self.impl(args, sys.stdin, sys.stdout))

    def impl(self, args: List[str], stdin, stdout):
        if len(args) > 1:
            print("exit: to many arguments", file=sys.stderr)
            return 1

        if len(args) == 1:
            return int(args[0])

        return 0

