import subprocess
from typing import List, Dict

from src.Executable import Executable


class External(Executable):
    def __init__(self, path: str):
        self.env: Dict[str, str] = dict()
        self.cwd = ""
        self.path: str = path

    def set_env(self, workdir: str, env: Dict[str, str]):
        self.env = env
        self.cwd = workdir

    def exec(self, args: List[str]) -> int:
        return subprocess.run([self.path, *args], env=self.env, cwd=self.cwd).returncode

    def exec_pipe(self, args: List[str], stdin: int) -> int:
        raise NotImplemented
