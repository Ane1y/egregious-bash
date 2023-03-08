import pytest

from src.Lexer import *

def test_quotes():
    command = "echo 'hello'"
    right_expr = [StrLex("echo"), Space(), Quoted("hello"), EndLine()]
    lexer = Lexer(command)
    assert list(lexer.get()) == right_expr

def test_doublequotes():
    command = "something \"hey this is quoted string!\" \"and one more\""
    right_expr = [StrLex("something"), Space(), DoubleQuoted("hey this is quoted string!"),
                  Space(), DoubleQuoted("and one more"), EndLine()]
    lexer = Lexer(command)
    assert list(lexer.get()) == right_expr

def test_quotes_without_spacing():
    command = "bop bop 'bip''bip'"
    right_expr = [StrLex("bop"), Space(), StrLex('bop'), Space(),
                  Quoted('bip'), Quoted('bip'), EndLine()]
    lexer = Lexer(command)
    assert list(lexer.get()) == right_expr

def test_different_quotes_without_spacing():
    command = "bop bop \"bip\"'bip'"
    right_expr = [StrLex("bop"), Space(), StrLex('bop'), Space(),
                  DoubleQuoted('bip'), Quoted('bip'), EndLine()]
    lexer = Lexer(command)
    assert list(lexer.get()) == right_expr

def test_double_quotes_without_spacing():
    command = "bop bop \"bip\"\"bip\""
    right_expr = [StrLex("bop"), Space(), StrLex('bop'), Space(),
                  DoubleQuoted('bip'), DoubleQuoted('bip'), EndLine()]
    lexer = Lexer(command)
    assert list(lexer.get()) == right_expr

def test_quotes_in_double_quotes():
    command = "bop bop \"b'i'p\"\"bip\""
    right_expr = [StrLex("bop"), Space(), StrLex('bop'), Space(),
                  DoubleQuoted('b\'i\'p'), DoubleQuoted('bip'), EndLine()]
    lexer = Lexer(command)
    assert list(lexer.get()) == right_expr
def test_double_quotes_in_quotes():
    command = "bop bop 'b\"i\"p'"
    right_expr = [StrLex("bop"), Space(), StrLex('bop'), Space(),
                  Quoted('b"i"p'), EndLine()]
    lexer = Lexer(command)
    assert list(lexer.get()) == right_expr

def test_pipe():
    command = "asd| zxc"
    right_expr = [StrLex("asd"), PipeChar(), Space(), StrLex("zxc"), EndLine()]
    lexer = Lexer(command)
    assert list(lexer.get()) == right_expr

def test_equals():
    command = "asd=123"
    right_expr = [StrLex("asd"), Equal(), StrLex("123"), EndLine()]
    lexer = Lexer(command)
    assert list(lexer.get()) == right_expr

def test_spacing():
    command = "asd  asd"
    right_expr = [StrLex("asd"), Space(), StrLex("asd"), EndLine()]
    lexer = Lexer(command)
    assert list(lexer.get()) == right_expr