import pylisper.interpreter.objects as obj
import pylisper.interpreter.symbols as sym
from pylisper.interpreter.exceptions import EvalTypeError, LogicError


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
    sym.CONS: _cons,
    sym.CDR: _cdr,
    sym.CAR: _car,
    sym.ATOM: _atom,
    sym.EQ: lambda a, b: a is b,
    sym.NULL: _null,
    sym.TRUE: True,
    sym.FALSE: False,
    sym.EQ_NUM: lambda a, b: a == b,
    sym.MINUS_NUM: lambda a, b: a - b,
    sym.PLUS_NUM: lambda a, b: a + b,
    sym.NOT: _not,
}
"""
A `dict` instance containing standard environment to init
global environment with.
"""
