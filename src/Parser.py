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
        token = next(self.it)

        if space(token):
            token = next(self.it)

        if pipeChar(token):
            raise ValueError("syntax error near |")

        name = ""
        pipe_queue = []

        while not(eof(token)): #Program level
            if not(endl(token)):
                if pipeChar(token) or pipe_queue:
                    self.form_cmd_to_pipe(pipe_queue)
                    token = next(self.it)

                if strLex(token) or name == "" and not delimeter(token):
                    name, token = self.read_name(token)

                if equal(token) or strLex(token):
                    token = self.read_cmd_or_assigment(name, token)
                    name = ""

            else:
                if pipe_queue:
                    self.form_cmd_to_pipe(pipe_queue)
                    yield Pipe(pipe_queue)
                else:
                    yield self.command_pack[0]
            #endl level


    def get(self) -> Program:
        return Program(self.get_iter())


    #helpers todo:create another class??
    def form_cmd_to_pipe(self, queue):
        for cmd in self.command_pack:
            queue.append(cmd)
        self.command_pack = []

    def read_str(self, init_value: str) -> (str, Lex):
        buf = next(self.it)
        value = init_value
        while strLex(buf):
            value += buf.text
            buf = next(self.it)
        return value, buf

    def read_name(self, next_token):
        if space(next_token):
            next_token = next(self.it)
        if equal(next_token):
            next_token.text = "="
        return self.read_str(next_token.text)

    def read_assigment(self) -> (str, Iterator[Lex]):
        buffer = next(self.it)
        if strLex(buffer):
            value, buffer = self.read_str(buffer.text)
        else:
            value = ""
        return value, buffer

    def read_args(self) -> (List[str], Lex):
        args = []
        buffer = next(self.it)
        while not (delimeter(buffer)):  # TODO:check types
            while strLex(buffer):
                arg, buffer = self.read_str(buffer.text)
                args.append(arg)
            if space(buffer):
                buffer = next(self.it)
        return args, buffer

    def read_cmd_or_assigment(self, name: str, next_token : Lex):
        # if asssigment
        # two possible variants: if second lexem in string is = then it s assigment, otherwise cmd
        if equal(next_token):
            value, next_token = self.read_assigment()
            self.command_pack.append(Assignment(name, value))
        # if cmd
        elif space(next_token):
            args, next_token = self.read_args()
            self.command_pack = [Cmd(self.command_pack, name, args)]
        return next_token
