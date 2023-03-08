from typing import Dict

from src.Executable import Executable


class Environment:
    def __init__(self, env: Dict[str, str]):
        self.dict = env.copy()

    def get_var(self, name: str) -> str:
        if name in self.dict:
            return self.dict[name]
        return ""

    def set_var(self, name: str, value: str):
        self.dict[name] = value

    def get_exec(self, name_or_path: str) -> Executable:
        raise NotImplemented
