import os
from typing import Dict, List, Optional
from src.Executable import Executable
from src.builtin import *
from src.External import External
from shutil import which


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

        exe: Optional[External] = None
        if os.path.exists(name_or_path):
            exe = External(name_or_path)

        else:
            for directory in self.__path():
                path = which(name_or_path, path=directory)
                if path is not None:
                    exe = External(path)

        if exe is not None:
            self.executables[name_or_path] = exe
            return exe

        raise FileNotFoundError

    def __path(self) -> List[str]:
        if 'PATH' in self.variables:
            return self.variables['PATH'].split(':')

        return [os.getcwd()]

    def __init_executables(self):
        self.executables['cat'] = Cat()
        self.executables['echo'] = Echo()
        self.executables['exit'] = Exit()
        self.executables['pwd'] = Pwd()
        self.executables['wc'] = Wc()
