import sys
from typing import List

from src.Executable import BuiltIn


class Echo(BuiltIn):
    def exec(self, args: List[str]) -> int:
        for text in args:
            print(text, end=" ")
        print()  # print new line char
        return 0

    def exec_pipe(self, args: List[str], stdin: int) -> int:
        raise NotImplemented
