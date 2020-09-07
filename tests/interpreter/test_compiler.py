import utils.strategies as st
from hypothesis import given

import pylisper.interpreter.objects as obj
from pylisper import ast
from pylisper.interpreter.compiler import ObjectCompiler


@given(st.integers())
def test_number_compilation(val):
    comp = ObjectCompiler()
    assert ast.Number(val).accept(comp) == obj.Number(val)


@given(st.symbols())
def test_symbol_compilation(val):
    comp = ObjectCompiler()
    node = ast.Symbol(val).accept(comp)
    assert isinstance(node, obj.Symbol)
    assert node.value == val


def test_empty_list_compilation():
    comp = ObjectCompiler()
    assert ast.List().accept(comp) is None


@given(st.lists(st.naturals(), min_size=1))
def test_non_empty_list_compilation(val):
    comp = ObjectCompiler()
    node = ast.List([x for x in map(ast.Number, val)]).accept(comp)
    assert isinstance(node, obj.Cell)
    comp_vals = [x.value for x in node]
    assert comp_vals == val
