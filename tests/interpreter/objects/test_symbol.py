from pylisper.interpreter.objects._symbol import Symbol

import utils.strategies as st
from hypothesis import given

@given(st.symbols())
def test_symbol_identity(val):
    assert Symbol(val) is Symbol(val)