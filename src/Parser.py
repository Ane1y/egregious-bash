from typing import Iterable, Union, List
from dataclasses import dataclass

from src.Lexer import Lex, Equal, StrLex, PipeChar, EndLine
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
        commands_pack = List[Union[Pipe, Cmd, Assignment]]
        buffer = next(self.lex)

        while not(eof(buffer)): #Program level
            if not(pipeChar(buffer)): # Cmd/Pipe level
                symbol = next(self.lex)
                if equal(symbol):
                    value = next(self.lex)
                    if strLex(value):

                        value += next(self.lex)
        #
        #
        # while not(isinstance(name, PipeChar)) and not(isinstance(name, EndLine)):
        #     if not(isinstance(name, StrLex)):
        #         raise ValueError(f"command not found {name}")
        #
        #     something = next(self.lex)
        #
        #     if isinstance(something, Equal):
        #         value = next(self.lex)
        #         if not(isinstance(value, StrLex)):
        #             raise ValueError("parse error near {value}")
        #         else:
        #             yield Assignment(name.text, value.text)
        #             name = next(self.lex)
        #
        #     else:
        #         pass


    def get(self) -> Program:
        return Program(self.get_iter())
