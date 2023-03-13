import pytest

from src.Expander import Expander
from src.Lexer import Lexer
from src.Parser import Parser, Assignment, Cmd, Pipe


def test_simple_cmd():
    lex = Lexer("echo bum asd")
    expander = Expander(lex.get())
    parser = Parser(expander.get())

    cmd = next(parser.get().commands)
    assert isinstance(cmd, Cmd)
    assert len(list(cmd.prefix)) == 0
    assert cmd.name == "echo"
    assert cmd.suffix == ["bum", "asd"]


def test_cmd_with_prefix():
    lex = Lexer("asd=456 bvd=789 echo bum asd")
    expander = Expander(lex.get())
    parser = Parser(expander.get())
    cmd = next(parser.get().commands)
    assert isinstance(cmd, Cmd)
    assert cmd.prefix == [Assignment("asd", "456"), Assignment("bvd", "789")]
    assert cmd.name == "echo"
    assert cmd.suffix == ["bum", "asd"]


def test_wrong_cmd_with_equals():
    lex = Lexer("=456 asd")
    expander = Expander(lex.get())
    parser = Parser(expander.get())

    cmd = next(parser.get().commands)
    assert isinstance(cmd, Cmd)
    assert cmd.prefix == []
    assert cmd.name == "=456"
    assert cmd.suffix == ["asd"]


def test_assigment():
    lex = Lexer("asd=123")
    expander = Expander(lex.get())
    parser = Parser(expander.get())

    cmd = next(parser.get().commands)
    assert isinstance(cmd, Assignment)
    assert cmd.name == "asd"
    assert cmd.value == "123"


def test_simple_pipe():
    lex = Lexer("asd=123 | echo qwe")
    expander = Expander(lex.get())
    parser = Parser(expander.get())

    cmd = next(parser.get().commands)
    assert isinstance(cmd, Pipe)
    assert cmd.commands == [Assignment("asd", "123"), Cmd([], "echo", ["qwe"])]


def test_pipe_without_spaces():
    lex = Lexer("asd=123|echo qwe")
    expander = Expander(lex.get())
    parser = Parser(expander.get())

    cmd = next(parser.get().commands)
    assert isinstance(cmd, Pipe)
    assert cmd.commands == [Assignment("asd", "123"), Cmd([], "echo", ["qwe"])]


def test_pipe_double_command():
    lex = Lexer("zch asd sdf | echo qwe")
    expander = Expander(lex.get())
    parser = Parser(expander.get())

    cmd = next(parser.get().commands)
    assert isinstance(cmd, Pipe)
    assert cmd.commands == [Cmd([], "zch", ["asd", "sdf"]), Cmd([], "echo", ["qwe"])]