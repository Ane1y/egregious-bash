from typing import Iterator

from src.Lexer import Lex, Equal, PipeChar, EndLine, EndOfFile, Str, Space


def equal(lex: Lex) -> bool:
    return isinstance(lex, Equal)

def space(lex: Lex) -> bool:
    return isinstance(lex, Space)


def pipeChar(lex: Lex) -> bool:
    return isinstance(lex, PipeChar)


def endl(lex: Lex) -> bool:
    return isinstance(lex, EndLine)


def eof(lex: Lex) -> bool:
    return isinstance(lex, EndOfFile)


def strLex(lex: Lex) -> bool:
    return isinstance(lex, Str)


def delimeter(lex: Lex) -> bool:
    return isinstance(lex, PipeChar) or isinstance(lex, EndLine) or isinstance(lex, EndOfFile)


def read_str(init_value: str, it: Iterator[Lex]) -> str:
    buf = next(it)
    value = init_value
    while strLex(buf):
        value += buf.text
        buf = next(it)
    return value