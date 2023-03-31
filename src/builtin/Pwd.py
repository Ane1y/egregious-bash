from typing import List

from src.Environment import Environment
from src.Executable import BuiltIn


class Pwd(BuiltIn):
    def impl(self, args: List[str], stdin, stdout) -> int:
        print(Environment.get_cwd(), file=stdout)
        return 0
