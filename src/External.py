import subprocess
from typing import List, Dict

from src.Executable import Executable


class External(Executable):
    def __init__(self, path: str):
        self.env: Dict[str, str] = dict()
        self.path: str = path

    def set_env(self, env: Dict[str, str]):
        self.env = env

    def exec(self, args: List[str]) -> int:
        return subprocess.run([self.path, *args], env=self.env).returncode

    def exec_pipe(self, args: List[str], stdin: int) -> int:
        raise NotImplemented
