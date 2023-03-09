from src.Lexer import Lex, Equal, PipeChar, EndLine, EndOfFile, Str


def equal(lex : Lex) -> bool:
    return isinstance(lex, Equal)

def pipeChar(lex : Lex) -> bool:
    return isinstance(lex, PipeChar)

def eoln(lex : Lex) -> bool:
    return isinstance(lex, EndLine)

def eof(lex : Lex) -> bool :
    return isinstance(lex, EndOfFile)

def strLex(lex : Lex) -> bool :
    return isinstance(lex, Str)
