import os
from typing import List

from src.Executable import BuiltIn


class Pwd(BuiltIn):
    def exec(self, args: List[str]) -> int:
        print(os.getcwd())
        return 0

    def exec_pipe(self, args: List[str], stdin: int) -> int:
        raise NotImplemented
