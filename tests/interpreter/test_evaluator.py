from unittest import mock

import pytest
import utils.strategies as st
from hypothesis import given

import pylisper.interpreter.objects as obj
from pylisper.interpreter.compiler import ObjectCompiler
from pylisper.interpreter.env import Env
from pylisper.interpreter.evaluator import Evaluator
from pylisper.interpreter.exceptions import EvaluationError
from pylisper.interpreter.std_env import STD_ENV
from pylisper.lexer import lexer
from pylisper.parser import parser

# arbitrarily chosen
RECURSION_LIMIT = 100


def eval(source, init_env=None):
    if init_env is None:
        init_env = Env(STD_ENV)
    evaluator = Evaluator(init_env)
    comp = ObjectCompiler()
    ast = parser.parse(lexer.lex(source))
    code = ast.accept(comp)
    return evaluator.eval(code)


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
    assert obj.Symbol(sym) in env
    assert env[obj.Symbol(sym)] == val


@given(st.naturals(), st.naturals())
def test_function_call(fst, snd):
    m = mock.Mock()
    env = Env({obj.Symbol("func"): m})
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
    env = Env({obj.Symbol("func"): m})
    eval(f"((lambda (x) (func x)) {val})", init_env=env)
    m.assert_called_once_with(val)


@given(st.naturals())
def test_lambda_env_capture(val):
    m = mock.Mock()
    env = Env({obj.Symbol("func"): m})
    eval(
        """
        (define a
            (lambda (x)
                (lambda () (func x))))
        """,
        init_env=env,
    )
    eval(f"(define b (a {val}))", init_env=env)
    eval("(b)", init_env=env)
    m.assert_called_once_with(val)


@given(st.naturals(max_value=RECURSION_LIMIT))
def test_recursive_function_call(val):
    m = mock.Mock()
    env = Env({obj.Symbol("func"): m, **STD_ENV})
    calls = [mock.call(x) for x in range(val, 0, -1)]
    eval(
        """
        (define a
            (lambda (acc _)
                (cond
                    ((= acc 0) #t)
                    (#t (a (- acc 1) (func acc))))))
        """,
        init_env=env,
    )
    assert eval(f"(a {val} (func {val}))", init_env=env)
    m.assert_has_calls(calls)


def test_against_env_reference_cycle():
    env = Env(STD_ENV)
    eval(
        """
        (define a
            (lambda (acc)
                (cond
                    ((= acc 0) #t)
                    (#t (a (- acc 1))))))
    """,
        init_env=env,
    )
    assert eval("(a 10)", env)
    eval(
        """
        (define a
            (lambda (acc)
                (cond
                    ((= acc 0) #t)
                    (#t (a (- acc 1))))))
    """,
        init_env=env,
    )
    assert eval("(a 10)", env)


@given(st.symbols(allow_numbers=False), st.naturals())
def test_set_form_evaluation(sym, val):
    env = Env()
    eval(f"(define {sym} (quote ()))", env)
    eval(f"(set! {sym} {val})", env)
    assert env[obj.Symbol(sym)] == val


@given(st.symbols(allow_numbers=False), st.naturals())
def test_set_form_setting_value_in_outer_scope(sym, val):
    env = Env()
    eval(f"(define {sym} (quote ()))", env)
    eval(
        f"""
        (define a (lambda () (set! {sym} {val})))
    """,
        env,
    )
    eval("(a)", env)
    assert env[obj.Symbol(sym)] == val


@given(st.symbols(allow_numbers=False), st.naturals(), st.naturals())
def test_set_form_setting_value_in_inner_scope(sym, outer, inner):
    m = mock.Mock()
    env = Env({obj.Symbol("func"): m})
    eval(f"(define {sym} {outer})", env)
    eval(
        f"""
        (define a
            (lambda ({sym})
                (begin
                    (set! {sym} {inner})
                    (func {sym}))))
    """,
        env,
    )
    eval("(a (quote ()))", env)
    m.assert_called_once_with(inner)
    assert env[obj.Symbol(sym)] == outer


@given(st.lists(st.naturals(), min_size=1), st.naturals())
def test_set_form_on_first_cell_in_list(init, val):
    env = Env(STD_ENV)
    list_vals = " ".join(map(str, init))
    eval(f"(define loc (quote ({list_vals})))", env)
    eval(f"(set! (car loc) {val})", env)
    assert env[obj.Symbol("loc")].value == val


@given(st.lists(st.naturals(), min_size=3), st.naturals())
def test_set_form_on_some_cell_in_list(init, val):
    env = Env(STD_ENV)
    list_vals = " ".join(map(str, init))
    eval(f"(define loc (quote ({list_vals})))", env)
    eval(f"(set! (car (cdr (cdr loc))) {val})", env)
    assert env[obj.Symbol("loc")].cdr.cdr.value == val
