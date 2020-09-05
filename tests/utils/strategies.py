# flake8: noqa
from hypothesis.strategies import *

from pylisper.lexer import TOKENS as _TOKENS


def symbols():
    return from_regex(_TOKENS["SYMBOL"], fullmatch=True)
