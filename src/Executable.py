import os
import sys
from abc import ABC, abstractmethod
from typing import List, Dict


class Executable(ABC):
    def __init__(self):
        self.return_code: int = -1

    @abstractmethod
    def set_env(self, workdir: str, env: Dict[str, str]):
        raise NotImplemented

    @abstractmethod
    def exec(self, args: List[str]) -> int:
        raise NotImplemented

    @abstractmethod
    def exec_pipe(self, args: List[str], stdin: int) -> int:
        """
        :param args: arguments to pass to a process
        :param stdin: input stream descriptor
        :return: output stream descriptor
        """
        raise NotImplemented


class BuiltIn(Executable, ABC):
    def __init__(self):
        super().__init__()
        self.cwd = ""

    def set_env(self, workdir: str, env: Dict[str, str]):
        self.cwd = workdir

    def exec(self, args: List[str]) -> int:
        return self.impl(args, sys.stdin, sys.stdout)

    def exec_pipe(self, args: List[str], stdin):
        r, w = os.pipe()
        stdout_write = os.fdopen(w, 'w+')
        stdout_read = os.fdopen(r, 'r+')
        self.return_code = self.impl(args, stdin, stdout_write)
        stdout_write.close()
        return stdout_read

    @abstractmethod
    def impl(self, args: List[str], stdin, stdout) -> int:
        raise NotImplemented
