import subprocess
from typing import List, Dict, Tuple
from src.Executable import Executable


class External(Executable):
    def __init__(self, path: str, *mandatory_args: str):
        super().__init__()
        self.env: Dict[str, str] = dict()
        self.cwd = ""
        self.path: str = path
        self.mandatory_args: Tuple[str, ...] = mandatory_args

    def set_env(self, workdir: str, env: Dict[str, str]):
        self.env = env
        self.cwd = workdir

    def exec(self, args: List[str]) -> int:
        return subprocess.run(
            [self.path, *self.mandatory_args, *args], env=self.env, cwd=self.cwd
        ).returncode

    def exec_pipe(self, args: List[str], stdin):
        proc = subprocess.Popen(
            [self.path, *self.mandatory_args, *args],
            env=self.env,
            cwd=self.cwd,
            stdin=stdin,
            stdout=subprocess.PIPE,
            text=True,
        )
        return proc.stdout
