import os
import subprocess
from typing import List
from src.Executable import BuiltIn
import sys


class Cat:
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


if __name__ == '__main__':
    args = sys.argv[1:]
    exit_code = 0
    if len(args) == 0:
        exit_code = Cat.user_input()
    else:
        exit_code = Cat.read_files(args)
