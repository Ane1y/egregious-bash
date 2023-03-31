import sys
from typing import List

from src.Executable import BuiltIn


class Cat(BuiltIn):
    def impl(self, args: List[str], stdin, stdout) -> int:
        if len(args) == 0:
            return Cat.user_input()
        return Cat.read_files(args)

    @staticmethod
    def user_input():
        try:
            for line in sys.stdin:
                print(line, end="")
        except EOFError:
            return 0

    @staticmethod
    def read_files(files: List[str]):
        ret_code = 0

        for file in files:
            try:
                with open(file, "r") as f:
                    print(f.read())
            except OSError as e:
                print(f"cat: {e.filename}: {e.strerror}", file=sys.stderr)
                ret_code = 1

        return ret_code
