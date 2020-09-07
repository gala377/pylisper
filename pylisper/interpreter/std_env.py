import pylisper.interpreter.objects as obj
from pylisper.interpreter.exceptions import EvalTypeError, LogicError


def _s(val: str):
    return obj.Symbol(val)


def _cons(car, cdr):
    if not isinstance(cdr, obj.Cell):
        raise EvalTypeError("second argument to cons has to be a list")
    return obj.Cell.cons(car, cdr)


def _car(cell):
    if cell is None:
        raise LogicError("car cannot be used on an empty list")
    if not isinstance(cell, obj.Cell):
        raise EvalTypeError("car can only be used on lists")
    return cell.car


def _cdr(cell):
    if cell is None:
        raise LogicError("cdr cannot be used on an empty list")
    if not isinstance(cell, obj.Cell):
        raise EvalTypeError("cdr can only be used on lists")
    return cell.cdr


def _atom(arg):
    return isinstance(arg, (obj.Number, obj.Symbol))


def _null(arg):
    return arg is None


def _not(arg):
    if not isinstance(arg, bool):
        raise EvalTypeError("not can only be called with bool value")
    return not arg


STD_ENV = {
    _s("cons"): _cons,
    _s("cdr"): _cdr,
    _s("car"): _car,
    _s("atom?"): _atom,
    _s("eq?"): lambda a, b: a is b,
    _s("null?"): _null,
    _s("#t"): True,
    _s("#f"): False,
    _s("="): lambda a, b: a == b,
    _s("-"): lambda a, b: a - b,
    _s("+"): lambda a, b: a + b,
    _s("not"): _not,
}
"""
A `dict` instance containing standard environment to init
global environment with.
"""
