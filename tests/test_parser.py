import pytest
from src.Lexer import Lexer
from src.Parser import Parser
def test_simple_echo():
    lex = Lexer("echo bum")
    parser = Parser(lex.get())
    for cmd in parser.get().commands:
        assert len(list(cmd.prefix)) == 0
        assert cmd.name == "echo"
        assert cmd.suffix == ["bum"]

def test_assigment():
    lex = Lexer("asd=123")
    parser = Parser(lex.get())
    for cmd in parser.get().commands:
        assert cmd.name == "asd"
        assert cmd.value == "123"
