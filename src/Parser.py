

from src.Lexer import Lex
from typing import Iterable, Union
from dataclasses import dataclass


@dataclass
class Assignment:
    name: str
    value: str


@dataclass
class Cmd:
    prefix: Iterable[Assignment]
    name: str
    suffix: Iterable[str]  # TODO: Confirm


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
        raise NotImplemented

    def get(self) -> Program:
        return Program(self.get_iter())
