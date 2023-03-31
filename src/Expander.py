import re

from src.Environment import Environment
from src.Lexer import Lex, Lexer, DoubleQuoted, EndOfFile
from typing import Iterable

from src.utils import doubleQuoted, eof, strLex


class Expander:
    def __init__(self, lex: Iterable[Lex]):
        self.lex = iter(lex)

    def make_subst(self, text: str) -> str:
        regex = re.compile(r"(\$\w+)")
        subts = []
        poses = []
        for mo in re.finditer(regex, text):
            value = mo.group()[1:]
            poses.append((mo.start(), mo.end()))
            subts.append(Environment.get_var(value))

        for i in reversed(range(len(subts))):
            start, end = poses[i]
            text = text[:start] + subts[i] + text[end:]

        return text

    def get(self) -> Iterable[Lex]:
        buf = next(self.lex)
        while not (eof(buf)):
            if doubleQuoted(buf):
                yield DoubleQuoted(self.make_subst(str(buf)))

            if strLex(buf):
                yield from Lexer(self.make_subst(str(buf))).get_substitution()

            if not (doubleQuoted(buf)) and not (strLex(buf)):
                yield buf
            buf = next(self.lex)
        yield EndOfFile()
