import os
from typing import Dict, List


class Environment:
    _variables: Dict[str, str]
    _spec_variables: Dict[str, str]

    @staticmethod
    def __init__(env: Dict[str, str]):
        Environment._spec_variables = env.copy()
        Environment._variables = dict()
        Environment._spec_variables['cwd'] = os.getcwd()

    @staticmethod
    def get_var(name: str) -> str:
        if name in Environment._variables:
            return Environment._variables[name]
        return ""

    @staticmethod
    def get_all_vars() -> Dict[str, str]:
        t = Environment._spec_variables.copy()
        t.update(Environment._variables)
        return t

    @staticmethod
    def get_cwd() -> str:
        return Environment._spec_variables["cwd"]

    @staticmethod
    def set_var(name: str, value: str):
        Environment._variables[name] = value

    @staticmethod
    def set_spec_var( name: str, value: str):
        Environment._spec_variables[name] = value

    @staticmethod
    def get_path() -> List[str]:
        if "PATH" in Environment._spec_variables:
            return Environment._spec_variables["PATH"].split(":")

        return [Environment.get_cwd()]

    @staticmethod
    def path_to(*args) -> str:
        curr_dir = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(curr_dir, *args)
