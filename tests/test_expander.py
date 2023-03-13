from src.Expander import Expander
from src.Lexer import Lexer, StrLex, EndLine, EndOfFile, Space, DoubleQuoted, Quoted
from src.Parser import Parser

def get_env():
    return {"a": "123", "asd": "456"}
def test_simple_substitution():
    lex = Lexer("$asd")
    expander = Expander(lex.get(), get_env())
    assert next(expander.get()).text == "456"
def test_double_substitution():
    lex = Lexer("$a $asd")
    expander = Expander(lex.get(), get_env())
    assert list(expander.get()) == [StrLex("123"), Space(), StrLex("456"), EndLine(), EndOfFile()]

def test_fused_substitution():
    lex = Lexer("$a$asd")
    expander = Expander(lex.get(), get_env())
    assert next(expander.get()).text == "123456"

def test_not_existing_substitution():
    lex = Lexer("$qwe$a")
    expander = Expander(lex.get(), get_env())
    assert next(expander.get()).text == "123"

def test_double_quoted():
    lex = Lexer("\"qwe $asd $a\" zx")
    expander = Expander(lex.get(), get_env())
    assert list(expander.get()) == [DoubleQuoted("qwe 456 123"), Space(), StrLex("zx"), EndLine(), EndOfFile()]

def test_single_quoted():
    lex = Lexer("'qwe $asd $a' zx")
    expander = Expander(lex.get(), get_env())
    assert list(expander.get()) == [Quoted("qwe $asd $a"), Space(), StrLex("zx"), EndLine(), EndOfFile()]

def test_single_and_double_quoted_in_one_cmd() :
    lex = Lexer("'qwe $asd'\"$asd some\" zx")
    expander = Expander(lex.get(), get_env())
    assert list(expander.get()) == [Quoted("qwe $asd"), DoubleQuoted("456 some"), Space(), StrLex("zx"), EndLine(), EndOfFile()]

