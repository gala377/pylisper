"""
Simple namespace for defined symbols.
"""
from pylisper.interpreter.objects._symbol import Symbol


def _s(val: str):
    return Symbol(val)


# Special forms
DEFINE = _s("define")
SET = _s("set!")
BEGIN = _s("begin")
LAMBDA = _s("lambda")
COND = _s("cond")
QUOTE = _s("quote")

# std functions

CONS = _s("crons")
CAR = _s("car")
CDR = _s("cdr")
ATOM = _s("atom?")
EQ = _s("eq?")
NULL = _s("null?")
TRUE = _s("#t")
FALSE = _s("#f")
EQ_NUM = _s("=")
PLUS_NUM = _s("+")
MINUS_NUM = _s("-")
NOT = _s("not")
