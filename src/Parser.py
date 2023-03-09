from typing import Iterable, Union, List
from dataclasses import dataclass

from utils import *

@dataclass
class Assignment:
    name: str
    value: str


@dataclass
class Cmd:
    prefix: Iterable[Assignment]
    name: str
    suffix: List[str]  # TODO: Confirm


@dataclass
class Pipe:
    commands: Iterable[Cmd]


@dataclass
class Program:
    commands: Iterable[Union[Pipe, Cmd, Assignment]]


class Parser:
    def __init__(self, lex: Iterable[Lex]):
        self.lex = lex

    def get_iter(self) -> Iterable[Union[Pipe, Cmd, Assignment]]:
        it = iter(self.lex)
        init = next(it)
        buffer = ""
        while strLex(init):
            buffer += init.text
            init = next(it)

        while not(eof(buffer)): #Program level
            commands_pack = List[Union[Pipe, Cmd, Assignment]]

            if not(endl(buffer)):

                if strLex(buffer): # Cmd/Pipe level
                    symbol = next(it)
                    # two possible variants: if second lexem in string is = then it s assigment, otherwise cmd
                    if equal(symbol):
                        value = next(it)
                        if strLex(value):
                            read_str(value.text, it)
                        else:
                            buffer = value
                            value = ""
                        commands_pack.append(Assignment(buffer, value))
                    # if cmd
                    if space(symbol):
                        args = []
                        args_value = next(it)
                        args_buffer = ""
                        while not(delimeter(args_value)): #TODO:check types
                            while not(space(args_value)):
                                args.append(read_str(args_value.text, it))
                                args_value = it
                        tmp = Cmd(commands_pack, buffer.text, args)
                        commands_pack = [tmp]
                        buffer = args_value

                # if pipeChar(buffer):



    def get(self) -> Program:
        return Program(self.get_iter())
