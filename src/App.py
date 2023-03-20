import os
import sys

from src.Parser import Parser, Program, Cmd, Pipe, Assignment
from src.Lexer import Lexer
from src.Expander import Expander
from src.Environment import Environment

from typing import Union, Iterable, Dict


class App:
    def __init__(self, env: Dict[str, str]):
        self.env = Environment(env)

    def run(self):
        while True:
            text = input(" > ")
            lexer = Lexer(text)
            expander = Expander(lexer.get())
            parser = Parser(expander.get())

            self.execute_program(parser.get())

    def execute_program(self, prog: Program):
        for cmd in prog.commands:
            self.execute_cmd(cmd)

    def execute_cmd(self, cmd: Union[Pipe | Cmd | Assignment]):
        if type(cmd) == Pipe:
            raise NotImplemented

        if type(cmd) == Assignment:
            self.env.set_var(cmd.name, cmd.value)
            return

        if type(cmd) == Cmd:
            try:
                executable = self.env.get_exec(cmd.name)

                env_vars: Dict[str, str] = self.env.variables.copy()
                for ass in cmd.prefix:
                    env_vars[ass.name] = ass.value

                executable.set_env(self.env.cwd, env_vars)
                executable.exec(cmd.suffix)
            except FileNotFoundError:
                print(f"ebash: {cmd.name}: can't file such executable", file=sys.stderr)

        else:
            raise ValueError(f"Unexpected type of cmd, got {type(cmd)}")


if __name__ == "__main__":
    App(dict(os.environ)).run()
