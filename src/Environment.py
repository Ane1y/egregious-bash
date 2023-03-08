from typing import Dict
from src.Executable import Executable
import src.builtin.Cat


class Environment:
    def __init__(self, env: Dict[str, str]):
        self.variables: Dict[str, str] = env.copy()
        self.executables: Dict[str, Executable] = dict()
        self.__init_executables()

    def get_var(self, name: str) -> str:
        if name in self.variables:
            return self.variables[name]
        return ""

    def set_var(self, name: str, value: str):
        self.variables[name] = value

    def get_exec(self, name_or_path: str) -> Executable:

        if name_or_path in self.executables:
            return self.executables[name_or_path]

        # TODO: Implement PATH search for executable
        raise NotImplemented

    def __init_executables(self):
        self.executables['cat'] = src.builtin.Cat.Cat()
