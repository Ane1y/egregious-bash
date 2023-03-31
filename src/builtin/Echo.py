from typing import List

from src.Executable import BuiltIn


class Echo(BuiltIn):
    def impl(self, args: List[str], stdin, stdout):
        for text in args:
            print(text, end=" ", file=stdout)
        print(file=stdout)  # print new line char
        return 0
