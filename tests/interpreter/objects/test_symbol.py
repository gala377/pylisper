import utils.strategies as st
from hypothesis import given

from pylisper.interpreter.objects._symbol import Symbol


@given(st.symbols())
def test_symbol_identity(val):
    assert Symbol(val) is Symbol(val)
