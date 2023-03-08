
from src.Lexer import Lex
from typing import Iterable


class Extender:

    def __init__(self, lex: Iterable[Lex]):
        raise NotImplemented

    def get(self) -> Iterable[Lex]:
        raise NotImplemented
