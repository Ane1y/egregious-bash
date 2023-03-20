from copy import copy
from typing import Iterable, Union, List, TypeAlias
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


CmdList: TypeAlias = List[Union[Assignment, Cmd, Pipe]]


class Parser:
    def __init__(self, lex: Iterable[Lex]):
        self.it = iter(lex)
        self.command_pack: CmdList = []
        self.token = next(self.it)
        self.next_token = next(self.it)
        self.bip = 234

    def next(self):
        """
        :return: update the pair of token (token, next_token)
        """
        self.token = self.next_token
        try:
            self.next_token = next(self.it)
        except:
            self.next_token = self.token

    def get_iter(self) -> Iterable[Pipe | Cmd | Assignment]:
        if space(self.token):
            self.next()

        if pipeChar(self.token):
            raise ValueError("syntax error near |")

        name: str = ""
        pipe_queue: CmdList = []

        while not (eof(self.token)):  # Program level
            if not (endl(self.token)):
                if pipeChar(self.token) or pipeChar(self.next_token) or pipe_queue:
                    self.form_cmd_to_pipe(pipe_queue)
                    self.next()

                if str_(self.token) or name == "" and not delimeter(self.token):
                    name = self.read_name()

                if equal(self.token) or space(self.token) or endl(self.token):
                    if equal(self.token):
                        value = self.read_assigment()
                        self.command_pack.append(Assignment(name, value))
                    else:
                        args = self.read_args()
                        self.command_pack = [Cmd(self.command_pack, name, args)]
                    name = ""
                # self.next()

            elif pipe_queue:
                self.form_cmd_to_pipe(pipe_queue)
                yield Pipe(pipe_queue)
            else:  # endl
                self.next()
                yield self.command_pack.pop(0)

        yield from self.command_pack

    def get(self) -> Program:
        return Program(self.get_iter())

    # helpers todo:create another class??
    def form_cmd_to_pipe(self, queue):
        for cmd in self.command_pack:
            queue.append(cmd)
        self.command_pack = []

    def read_str(self) -> str:
        value = ""
        while str_(self.token):
            value += str(self.token)
            self.next()
        return value

    def read_name(self):
        if space(self.token):  # skip spaces
            self.next()
        return self.read_str()

    def read_assigment(self) -> str:
        if str_(self.token):
            value = self.read_str()
        else:
            value = ""
        return value

    def read_args(self) -> List[str]:
        args = []
        while not (delimeter(self.token)):
            while str_(self.token):
                arg = self.read_str()
                args.append(arg)
            if space(self.token):
                self.next()
        return args
