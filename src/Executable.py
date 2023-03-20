from abc import ABC, abstractmethod
from typing import List, Dict


class Executable(ABC):
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
        self.cwd = ""

    def set_env(self, workdir: str, env: Dict[str, str]):
        self.cwd = workdir
