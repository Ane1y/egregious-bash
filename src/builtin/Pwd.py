from typing import List
from Executable import BuiltIn


class Pwd(BuiltIn):
    def impl(self, args: List[str], stdin, stdout) -> int:
        print(self.cwd, file=stdout)
        return 0
