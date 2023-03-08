
from dataclasses import dataclass
from typing import Iterable


class Lex:
    pass


class Space(Lex):
    pass


class Equal(Lex):
    pass


class Pipe(Lex):
    pass


class EndLine(Lex):
    pass


class EndOfFile(Lex):
    pass


@dataclass
class Str(Lex):
    text: str


class Quoted(Str):
    pass


class DoubleQuoted(Str):
    pass


@dataclass
class StrLex(Lex):
    text: str


class Lexer:

    def __init__(self, text: str):
        self.text = text

    def get(self) -> Iterable[Lex]:
        raise NotImplemented
