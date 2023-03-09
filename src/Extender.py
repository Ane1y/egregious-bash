from src.Lexer import Lex
from typing import Iterable


class Extender:
    def __init__(self, lex: Iterable[Lex]):
        self.lex = lex

    def get(self) -> Iterable[Lex]:
        # Placeholder
        # TODO: Implement extension
        return self.lex
