from src.Executable import Executable


class Environment:

    def get_var(self, name: str) -> str:
        raise NotImplemented

    def set_var(self, name: str, value: str):
        raise NotImplemented

    def get_exec(self, name_or_path: str) -> Executable:
        raise NotImplemented
