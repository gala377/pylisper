import utils.strategies as st
from hypothesis import given

from pylisper.lexer import lexer


def assert_token(tok, val, type):
    assert tok.value == val
    assert tok.name == type


@given(st.integers(min_value=0))
def test_integers(val):
    tok, *_ = lexer.lex(str(val))
    assert_token(tok, str(val), "SYMBOL")


@given(st.symbol())
def test_symbols(val):
    tok, *_ = lexer.lex(val)
    assert_token(tok, val, "SYMBOL")


def test_parenthesis():
    lpar, rpar = lexer.lex("()")
    assert_token(lpar, "(", "LPAREN")
    assert_token(rpar, ")", "RPAREN")


@given(st.symbol(), st.text())
def test_comments(val, comment):
    val_comment = f"{val};{comment}"
    tokens = [t for t in lexer.lex(val_comment)]
    assert len(tokens) == 1
    assert_token(tokens[0], val, "SYMBOL")


@given(st.lists(st.symbol()))
def test_list_of_symbols(vals):
    vals = ["("] + vals + [")"]
    vals = zip(lexer.lex(" ".join(vals)), vals)
    par, *vals = vals
    assert_token(par[0], "(", "LPAREN")
    par = vals.pop()
    assert_token(par[0], ")", "RPAREN")
    for tok, v in vals:
        assert_token(tok, v, "SYMBOL")
