import os

from src.Parser import Parser, Program, Cmd, Pipe, Assignment
from src.Lexer import Lexer
from src.Extender import Extender
from src.Executable import Executable
from src.Environment import Environment

from typing import Union, Iterable


class App:
    def __init__(self):
        self.env = Environment(dict(os.environ))

    def run(self):
        text = input(" > ")
        lexer = Lexer(text)
        extender = Extender(lexer.get())
        parser = Parser(extender.get())

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
            executable = self.env.get_exec(cmd.name)

            cmd_env = Environment(self.env.dict)
            for ass in cmd.prefix:
                cmd_env.set_var(ass.name, ass.value)

            executable.set_env(cmd_env)
            executable.exec(cmd.suffix)

        raise ValueError(f'Unexpected type of cmd, got {type(cmd)}')


if __name__ == '__main__':
    App().run()
