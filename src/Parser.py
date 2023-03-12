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
        self.token = next(self.it)
        self.next_token = next(self.it)

    def next(self):
        """
        :return: update the pair of token (token, next_token)
        """
        self.token = self.next_token
        try:
            self.next_token = next(self.it)
        except:
            self.next_token = self.token

    def get_iter(self) -> Pipe | Cmd | Assignment:
        if space(self.token):
            self.next()

        if pipeChar(self.token):
            raise ValueError("syntax error near |")

        name = ""
        pipe_queue = []

        while not(eof(self.token)): #Program level
            if not(endl(self.token)):
                if pipeChar(self.token) or pipeChar(self.next_token) or pipe_queue:
                    self.form_cmd_to_pipe(pipe_queue)
                    self.next()

                if strLex(self.token) or name == "" and not delimeter(self.token):
                    name = self.read_name()

                if equal(self.token) or space(self.token):
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

    def read_str(self, init_value: str) -> str:
        self.next()
        value = init_value
        while strLex(self.token):
            value += self.token.text
            self.next()
        return value

    def read_name(self):
        if space(self.token):
            self.next()
        if equal(self.token):
            self.token.text = "="
        return self.read_str(self.token.text)

    def read_assigment(self) -> str:
        self.next()
        if strLex(self.token):
            value = self.read_str(self.token.text)
        else:
            value = ""
        return value

    def read_args(self) -> List[str]:
        args = []
        self.next()
        while not (delimeter(self.token)):
            while strLex(self.token):
                arg = self.read_str(self.token.text)
                args.append(arg)
            if space(self.token):
                self.next()
        return args
