import pytest
import utils.strategies as st
from hypothesis import given
from unittest import mock

from pylisper import ast
from pylisper.interpreter.ast_walk import AstWalkEvaluator
from pylisper.interpreter.env import STD_ENV, Env
from pylisper.interpreter.exceptions import EvaluationError
from pylisper.lexer import lexer
from pylisper.parser import parser

# arbitrarily chosen
RECURSION_LIMIT = 100

def eval(source, init_env=None):
    if init_env is None:
        init_env = Env(STD_ENV)
    visit = AstWalkEvaluator(init_env)
    ast = parser.parse(lexer.lex(source))
    return ast.accept(visit)


@given(st.naturals())
def test_number_evaluation(val):
    assert eval(str(val)) == val


@given(st.symbols(allow_numbers=False))
def test_unknown_symbol_evaluation(val):
    with pytest.raises(EvaluationError):
        eval(val)


@given(st.symbols(allow_numbers=False), st.naturals())
def test_symbol_definition(sym, val):
    env = Env()
    eval(f"(define {sym} {val})", init_env=env)
    assert ast.Symbol(sym) in env
    assert env[ast.Symbol(sym)] == val


@given(st.naturals(), st.naturals())
def test_function_call(fst, snd):
    m = mock.Mock()
    env = Env({ast.Symbol("func"): m})
    eval(f"(func {fst} {snd})", init_env=env)
    m.assert_called_once_with(fst, snd)


@given(st.symbols(allow_numbers=False), st.naturals())
def test_symbol_evaluation(sym, val):
    env = Env()
    eval(f"(define {sym} {val})", init_env=env)
    assert eval(sym, init_env=env) == val

@given(st.naturals())
def test_lambda_evaluation(val):
    m = mock.Mock()
    env = Env({ast.Symbol("func"): m})
    eval(f"((lambda (x) (func x)) {val})", init_env=env)
    m.assert_called_once_with(val)

@given(st.naturals())
def test_lambda_env_capture(val):
    m = mock.Mock()
    env = Env({ast.Symbol("func"): m})
    eval("""
        (define a 
            (lambda (x) 
                (lambda () (func x))))
    """, init_env=env)
    eval(f"(define b (a {val}))", init_env=env)
    eval(f"(b)", init_env=env)
    m.assert_called_once_with(val)
