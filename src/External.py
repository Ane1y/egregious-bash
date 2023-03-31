import subprocess
from typing import List, Dict, Tuple

from src.Environment import Environment
from src.Executable import Executable


class External(Executable):
    def __init__(self, path: str, *mandatory_args: str):
        super().__init__()
        self.local_env: Dict[str, str] = dict()
        self.path: str = path
        self.mandatory_args: Tuple[str, ...] = mandatory_args

    def set_local_env(self, env: Dict[str, str]):
        self.local_env = Environment.get_all_vars()
        self.local_env.update(env)

    def exec(self, args: List[str]) -> int:
        return subprocess.run(
            [self.path, *self.mandatory_args, *args],
            env=self.local_env,
            cwd=Environment.get_cwd()
        ).returncode

    def exec_pipe(self, args: List[str], stdin):
        proc = subprocess.Popen(
            [self.path, *self.mandatory_args, *args],
            env=self.local_env,
            cwd=Environment.get_cwd(),
            stdin=stdin,
            stdout=subprocess.PIPE,
            text=True,
        )
        return proc.stdout
