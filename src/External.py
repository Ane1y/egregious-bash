import subprocess
from typing import List, Optional

from src.Environment import Environment
from src.Executable import Executable


class External(Executable):
    def __init__(self, path: str):
        self.env: Optional[Environment] = None
        self.path: str = path

    def set_env(self, env: Environment):
        self.env = env

    def exec(self, args: List[str]) -> int:
        return subprocess.run([self.path, *args], env=self.env.variables).returncode

    def exec_pipe(self, args: List[str], stdin: int) -> int:
        raise NotImplemented
