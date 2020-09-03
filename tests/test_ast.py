from hypothesis import given, example
import hypothesis.strategies as st

from pylisper.ast import Symbol

@given(st.text(min_size=1))
def test_symbol_identity(s):
    assert Symbol(s) is Symbol(s)