from typing import List
from src.Executable import BuiltIn
import sys


class Cat(BuiltIn):
    def exec(self, args: List[str]) -> int:
        if len(args) == 0:
            return Cat.user_input()
        return Cat.read_files(args)

    def exec_pipe(self, args: List[str], stdin: int) -> int:
        raise NotImplemented

    @staticmethod
    def user_input():
        try:
            while True:
                text = input()
                print(text)
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
