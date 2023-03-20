import re

from Lexer import Lex, Lexer, DoubleQuoted, EndOfFile
from typing import Iterable, Dict

from utils import doubleQuoted, eof, strLex, quoted, delimeter


class Expander:
    def __init__(self, lex: Iterable[Lex], env: Dict[str, str] = dict()):
        self.lex = iter(lex)
        self.env = env

    def make_subst(self, text: str) -> str:
        regex = re.compile(r"(\$[A-Za-z0-9]+)")
        subts = []
        poses = []
        for mo in re.finditer(regex, text):
            value = mo.group()[1:]
            poses.append((mo.start(), mo.end()))
            subts.append(self.env[value] if value in self.env else "")

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
