from copy import copy
from typing import Iterable, Union, List
from dataclasses import dataclass

from src.utils import *

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
        self.it = iter(lex)
        self.command_pack = []

    def get_iter(self) -> Pipe | Cmd | Assignment:
        next_token = next(self.it)

        if space(next_token):
            next_token = next(self.it)

        if pipeChar(next_token):
            raise ValueError("syntax error near |")

        while not(eof(next_token)): #Program level
            if not(endl(next_token)):
                if pipeChar(next_token):
                    lhs = copy(self.command_pack)
                    next_token = self.read_cmd_or_assigment(name, next_token, self.it)
                    self.command_pack = [Pipe(lhs, self.command_pack)]

                if strLex(next_token) or name == "":
                    if space(next_token):
                        next_token = next(self.it)
                    name, next_token = self.read_str(next_token.text, self.it)

                if equal(next_token) or space(next_token):
                    next_token = self.read_cmd_or_assigment(name, next_token, self.it)

                name = ""
            else:
                yield self.command_pack[0]
            #endl level


    def get(self) -> Program:
        return Program(self.get_iter())


    #helpers todo:create another class??
    def read_str(self, init_value: str, it: Iterator[Lex]) -> (str, Lex):
        buf = next(it)
        value = init_value
        while strLex(buf):
            value += buf.text
            buf = next(it)
        return value, buf

    def read_assigment(self, it: Iterator[Lex]) -> (str, Iterator[Lex]):
        buffer = next(it)
        if strLex(buffer):
            value, buffer = self.read_str(buffer.text, it)
        else:
            value = ""
        return value, buffer

    def read_args(self, it: Iterator[Lex]) -> (List[str], Lex):
        args = []
        buffer = next(it)
        while not (delimeter(buffer)):  # TODO:check types
            while strLex(buffer):
                arg, buffer = self.read_str(buffer.text, it)
                args.append(arg)
            if space(buffer):
                buffer = next(it)
        return args, buffer

    def read_cmd_or_assigment(self, name: str, next_token : Lex, it: Iterator[Lex]):
        # if asssigment
        # two possible variants: if second lexem in string is = then it s assigment, otherwise cmd
        if equal(next_token):
            value, next_token = self.read_assigment(it)
            self.command_pack.append(Assignment(name, value))
        # if cmd
        elif space(next_token):
            args, next_token = self.read_args(it)
            self.command_pack = [Cmd(self.command_pack, name, args)]
        return next_token
