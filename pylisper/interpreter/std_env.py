import pylisper.interpreter.objects as obj
from pylisper import ast
from pylisper.interpreter.exceptions import EvaluationError


def _s(val: str):
    return obj.Symbol(val)


def _cons(car, cdr):
    if not isinstance(cdr, obj.Cell):
        raise EvaluationError("second argument to cons has to be a list")
    return obj.Cell.cons(car, cdr)


def _car(cell):
    if cell is None:
        raise EvaluationError("car cannot be used on an empty list")
    if not isinstance(cell, obj.Cell):
        raise EvaluationError("car can only be used on lists")
    # TODO: we need to return a reference to a cell
    # however in normal context a reference to a cell should
    # evaluate to the underlaying value
    # only set! treats it as a memory location
    return cell.car


def _cdr(list):
    if not isinstance(list, ast.List):
        raise EvaluationError("cdr can only be used on lists")
    if list.empty:
        raise EvaluationError("cdr cannot be used on an empty list")
    return ast.List(list.exprs[1:])


def _atom(arg):
    return isinstance(arg, (ast.Number, ast.String, ast.Symbol))


def _null(arg):
    if not isinstance(arg, ast.List):
        return False
    return arg.empty


def _error(msg):
    raise EvaluationError(str(msg))


STD_ENV = {
    _s("cons"): _cons,
    _s("cdr"): _cdr,
    _s("car"): _car,
    _s("atom?"): _atom,
    _s("eq?"): lambda a, b: a is b,
    _s("null?"): _null,
    _s("error"): _error,
    _s("#t"): True,
    _s("#f"): False,
    _s("="): lambda a, b: a == b,
    _s("-"): lambda a, b: a - b,
    _s("+"): lambda a, b: a + b,
}
"""
A `dict` instance containing standard environment to init
global environment with.
"""
