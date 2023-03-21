from typing import Iterator

from src.Lexer import (
    Lex,
    Equal,
    PipeChar,
    EndLine,
    EndOfFile,
    Str,
    Space,
    StrLex,
    DoubleQuoted,
    Quoted,
)


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


def str_(lex: Lex) -> bool:
    return issubclass(type(lex), Str)


def delimeter(lex: Lex) -> bool:
    return (
        isinstance(lex, PipeChar)
        or isinstance(lex, EndLine)
        or isinstance(lex, EndOfFile)
    )


def doubleQuoted(lex: Lex) -> bool:
    return isinstance(lex, DoubleQuoted)


def quoted(lex: Lex) -> bool:
    return isinstance(lex, Quoted)


def strLex(lex: Lex) -> bool:
    return isinstance(lex, StrLex)
