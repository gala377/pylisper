from hypothesis import given
from unittest import mock
import utils.strategies as st

from pylisper import ast


@given(st.text(min_size=1))
def test_ast_symbol_identity(s):
    assert ast.Symbol(s) is ast.Symbol(s)

@given(st.lists(st.none(), min_size=1))
def test_filled_ast_list_is_not_empty(val):
    l = ast.List(val)
    assert len(l) > 0
    assert not l.empty

def test_empty_ast_list_is_empty():
    l = ast.List()
    assert len(l) == 0
    assert l.empty

def test_ast_list_from_empty_list_is_empty():
    l = ast.List([])
    assert len(l) == 0
    assert l.empty

def test_ast_list_visits_proper_method():
    m = mock.Mock()
    n = ast.List()
    n.accept(m)
    m.visit_list.assert_called_once_with(n)

@given(st.symbols())
def test_ast_symbol_visits_proper_method(val):
    m = mock.Mock()
    n = ast.Symbol(val)
    n.accept(m)
    m.visit_symbol.assert_called_once_with(n)

@given(st.integers())
def test_ast_list_visits_proper_method(val):
    m = mock.Mock()
    n = ast.Number(val)
    n.accept(m)
    m.visit_number.assert_called_once_with(n)
