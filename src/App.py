import os
import sys
from shutil import which
from typing import Dict, List, Optional

from src.Environment import Environment
from src.Executable import Executable
from src.Expander import Expander
from src.External import External
from src.Lexer import Lexer
from src.Parser import Parser, Program, Cmd, Pipe, Assignment


class App:
    def __init__(self, env: Dict[str, str], executables: Dict[str, Executable]):
        Environment(env)
        self.executables: Dict[str, Executable] = executables
        self.last_return: int = 0

    def execute_args(self, args: List[str]):
        cmd = Cmd([], args[0], args[1:])
        try:
            executable = self.executable_from_cmd(cmd)
            executable.exec(cmd.suffix)
        except FileNotFoundError:
            print(f"{cmd.name}: can't find such executable", file=sys.stderr)

    def run(self):
        while True:
            try:
                text = input(f"{Environment.get_cwd()}> ")
                lexer = Lexer(text)
                expander = Expander(lexer.get())
                parser = Parser(expander.get())

                self.execute_program(parser.get())
            except EOFError:
                print("exit")
                return

    def execute_program(self, prog: Program):
        for cmd in prog.commands:
            if type(cmd) == Assignment:
                Environment.set_var(cmd.name, cmd.value)
                return

            if type(cmd) == Pipe:
                self.execute_pipe(cmd)
                return

            if type(cmd) == Cmd:
                try:
                    executable = self.executable_from_cmd(cmd)
                    self.last_return = executable.exec(cmd.suffix)
                except FileNotFoundError as e:
                    print(
                        f"ebash: {cmd.name}: can't find such executable",
                        file=sys.stderr,
                    )
                return

            raise ValueError(f"Unexpected type of cmd, got {type(cmd)}")

    def execute_pipe(self, pipe: Pipe):
        last_output = sys.stdin
        executable = None
        for cmd in pipe.commands:
            if type(cmd) == Cmd:  # Lonely assignments are ignored
                try:
                    executable = self.executable_from_cmd(cmd)
                    last_output = executable.exec_pipe(cmd.suffix, last_output)
                except FileNotFoundError:
                    print(
                        f"ebash: {cmd.name}: can't find such executable",
                        file=sys.stderr,
                    )
                    return

        for line in last_output:
            sys.stdout.write(line)

        self.last_return = executable.return_code if executable else 0

    def executable_from_cmd(self, cmd: Cmd) -> Executable:
        executable = self.get_exec(cmd.name)

        env_vars: Dict[str, str] = dict()
        for ass in cmd.prefix:
            env_vars[ass.name] = ass.value

        executable.set_local_env(env_vars)
        return executable

    def get_exec(self, name_or_path: str) -> Executable:
        if name_or_path in self.executables:
            return self.executables[name_or_path]

        exe: Optional[External] = None
        if os.path.exists(name_or_path):
            exe = External(name_or_path)

        else:
            for directory in Environment.get_path():
                path = which(name_or_path, path=directory)
                if path is not None:
                    exe = External(path)

        if exe is not None:
            self.executables[name_or_path] = exe
            return exe

        raise FileNotFoundError
