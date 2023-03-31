import subprocess
import sys
from abc import ABC, abstractmethod
from typing import List, Dict

from src.Environment import Environment


class Executable(ABC):
    def __init__(self):
        self.return_code: int = -1

    @abstractmethod
    def set_local_env(self, env: Dict[str, str]):
        raise NotImplemented

    @abstractmethod
    def exec(self, args: List[str]) -> int:
        raise NotImplemented

    @abstractmethod
    def exec_pipe(self, args: List[str], stdin):
        """
        :param args: arguments to pass to a process
        :param stdin: input stream descriptor
        :return: output stream descriptor
        """
        raise NotImplemented


class BuiltIn(Executable, ABC):
    def __init__(self):
        super().__init__()

    def set_local_env(self, env: Dict[str, str]):
        pass

    def exec(self, args: List[str]) -> int:
        return self.impl(args, sys.stdin, sys.stdout)

    def exec_pipe(self, args: List[str], stdin):
        name = self.__class__.__name__.lower()
        proc = subprocess.Popen(
            [sys.executable, "-m", "src", name, *args],
            cwd=Environment.get_cwd(),
            stdin=stdin,
            stdout=subprocess.PIPE,
            text=True,
        )
        return proc.stdout

    @abstractmethod
    def impl(self, args: List[str], stdin, stdout) -> int:
        raise NotImplemented
