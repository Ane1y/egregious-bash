import pytest
from src.Lexer import Lexer
from src.Parser import Parser, Assignment, Cmd


def test_simple_cmd():
    lex = Lexer("echo bum asd")
    parser = Parser(lex.get())
    cmd = next(parser.get().commands)
    assert isinstance(cmd, Cmd)
    assert len(list(cmd.prefix)) == 0
    assert cmd.name == "echo"
    assert cmd.suffix == ["bum", "asd"]

def test_cmd_with_prefix():
    lex = Lexer("asd=456 bvd=789 echo bum asd")
    parser = Parser(lex.get())
    cmd = next(parser.get().commands)
    assert isinstance(cmd, Cmd)
    assert cmd.prefix == [Assignment("asd", "456"), Assignment("bvd", "789")]
    assert cmd.name == "echo"
    assert cmd.suffix == ["bum", "asd"]

def test_assigment():
    lex = Lexer("asd=123")
    parser = Parser(lex.get())
    cmd = next(parser.get().commands)
    assert isinstance(cmd, Assignment)
    assert cmd.name == "asd"
    assert cmd.value == "123"

def test_simple_pipe():
    lex = Lexer("asd=123")
    parser = Parser(lex.get())
    cmd = next(parser.get().commands)
    assert cmd.name == "asd"
    assert cmd.value == "123"