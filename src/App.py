import os
import sys

from Parser import Parser, Program, Cmd, Pipe, Assignment
from Lexer import Lexer
from Expander import Expander
from Environment import Environment
from Executable import Executable

from typing import Dict


class App:
    def __init__(self, env: Dict[str, str]):
        self.env = Environment(env)
        self.last_return: int = 0

    def run(self):
        while True:
            text = input(" > ")
            lexer = Lexer(text)
            expander = Expander(lexer.get(), self.env.variables)
            parser = Parser(expander.get())

            self.execute_program(parser.get())

    def execute_program(self, prog: Program):
        for cmd in prog.commands:
            if type(cmd) == Assignment:
                self.env.set_var(cmd.name, cmd.value)
                return

            if type(cmd) == Pipe:
                self.execute_pipe(cmd)
                return

            if type(cmd) == Cmd:
                try:
                    executable = self.executable_from_cmd(cmd)
                    self.last_return = executable.exec(cmd.suffix)
                except FileNotFoundError:
                    print(f"ebash: {cmd.name}: can't find such executable", file=sys.stderr)
                return

            raise ValueError(f"Unexpected type of cmd, got {type(cmd)}")

    def execute_pipe(self, pipe: Pipe):
        last_output = sys.stdin
        executable = None
        for cmd in pipe.commands:
            if type(cmd) == Cmd:  # Lonely assignments are ignored
                executable = self.executable_from_cmd(cmd)
                last_output = executable.exec_pipe(cmd.suffix, last_output)

        for line in last_output:
            sys.stdout.write(line)

        self.last_return = executable.return_code if executable else 0

    def executable_from_cmd(self, cmd: Cmd) -> Executable:
        executable = self.env.get_exec(cmd.name)

        env_vars: Dict[str, str] = self.env.variables.copy()
        for ass in cmd.prefix:
            env_vars[ass.name] = ass.value

        executable.set_env(self.env.cwd, env_vars)
        return executable


if __name__ == "__main__":
    App(dict(os.environ)).run()
