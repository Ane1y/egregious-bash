
from abc import ABC, abstractmethod
from typing import Iterable


class Executable(ABC):

    @abstractmethod
    def exec(self, args: Iterable[str]) -> int:
        raise NotImplemented

    @abstractmethod
    def exec_pipe(self, args: Iterable[str], stdin: int) -> int:
        """
        :param args: arguments to pass to a process
        :param stdin: input stream descriptor
        :return: output stream descriptor
        """
        raise NotImplemented


class BuiltIn(Executable, ABC):
    pass
