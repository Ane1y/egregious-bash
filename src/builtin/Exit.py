import sys
from typing import List

from src.Executable import BuiltIn


class Exit(BuiltIn):
    def exec(self, args: List[str]) -> int:
        if len(args) > 1:
            print("exit: to many arguments", file=sys.stderr)
            return 1

        if len(args) == 1:
            sys.exit(int(args[0]))

        sys.exit(0)

    def exec_pipe(self, args: List[str], stdin: int) -> int:
        raise NotImplemented
