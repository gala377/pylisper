# flake8: noqa
from hypothesis.strategies import *

from pylisper.lexer import TOKENS as _TOKENS


def symbols(allow_numbers=True):
    patt = _TOKENS["SYMBOL"]
    if not allow_numbers:
        patt += r"""[^)('"`,;\s\r\d)]"""
    return from_regex(patt, fullmatch=True)


def naturals(max_value=None):
    return integers(min_value=0, max_value=max_value)
