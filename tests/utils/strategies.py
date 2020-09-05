# flake8: noqa
from hypothesis.strategies import *

from pylisper.lexer import TOKENS as _TOKENS


def symbol():
    return from_regex(_TOKENS["SYMBOL"], fullmatch=True)
