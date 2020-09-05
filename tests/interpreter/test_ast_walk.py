import pytest
import utils.strategies as st
from hypothesis import assume, given

from pylisper import ast
from pylisper.interpreter.ast_walk import AstWalkEvaluator
from pylisper.interpreter.env import Env, STD_ENV
from pylisper.interpreter.exceptions import EvaluationError
from pylisper.lexer import lexer
from pylisper.parser import parser


def eval(source):
    visit = AstWalkEvaluator(Env(STD_ENV))
    ast = parser.parse(lexer.lex(source))
    return ast.accept(visit)


@given(st.integers(min_value=0))
def test_number_evaluation(val):
    assert eval(str(val)) == val


@given(st.symbols(allow_numbers=False))
def test_unknown_symbol_evaluation(val):
    assume(ast.Symbol(val) not in STD_ENV)
    with pytest.raises(EvaluationError):
        eval(val)
