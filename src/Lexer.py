import re
import shlex

from dataclasses import dataclass
from typing import Iterable


class Lex:
    pass

# to compare symbols in tests
class ServiceSymbols(Lex):
    def __eq__(self, other):
        if type(self) is type(other):
            return True
        return False

class Space(ServiceSymbols):
    def __str__(self):
        return "space"


class Equal(ServiceSymbols):
    def __str__(self):
        return "="


class PipeChar(ServiceSymbols):
    def __str__(self):
        return "|"


class EndLine(ServiceSymbols):
    def __str__(self):
        return "endl"


class EndOfFile(ServiceSymbols):
    def __str__(self):
        return "eof"


@dataclass
class Str(Lex):
    text: str


class Quoted(Str):
    pass


class DoubleQuoted(Str):
    pass


@dataclass
class StrLex(Str):
    pass


class Lexer:
    def __init__(self, text: str):
        self.words = re.split(r'(\s+|=|[|]|"[^"]*"|\'[^\']*\')', text)
        # self.words = list(shlex.shlex(text, punctuation_chars=" "))
        self.text = text
    def get_lex(self, word: str) -> Lex:
        if word == "=":
            return Equal()

        if word == "|":
            return PipeChar()

        if word[0] == "\"":
            return DoubleQuoted(word[1:-1])

        if word[0] == "'":
            return Quoted(word[1:-1])

        if re.compile(r'\s+').match(word):
            return Space()

        return StrLex(word)

    def get(self) -> Iterable[Lex]:
        for word in self.words:
            if word != "":
                yield self.get_lex(word)
            else:
                continue
        yield EndLine()


if __name__ == "__main__" :
    text = input()
    lexer = Lexer(text)
    print(list(lexer.get()))
