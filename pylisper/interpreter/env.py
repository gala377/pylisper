from __future__ import annotations

from collections import UserDict
from typing import Mapping, Optional

from pylisper import ast
from pylisper.interpreter.exceptions import EvaluationError
from pylisper.interpreter import objects as obj

class Env(UserDict):
    def __init__(self, init: Optional[Mapping] = None, parent: Optional[Env] = None):
        super().__init__(init)
        self.parent = parent

    @property
    def is_global(self) -> bool:
        return self.parent is None

    def lookup(self, sym: ast.Symbol) -> Env:
        assert isinstance(sym, ast.Symbol)
        if sym in self.data:
            return self
        return None if self.parent is None else self.parent.lookup(sym)

    def __repr__(self):
        r = repr(self.data)
        if self.parent is not None:
            r = f"{r} => {repr(self.parent)}"
        return


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
    ast.Symbol("cons"): _cons,
    ast.Symbol("cdr"): _cdr,
    ast.Symbol("car"): _car,
    ast.Symbol("atom?"): _atom,
    ast.Symbol("eq?"): lambda a, b: a is b,
    ast.Symbol("null?"): _null,
    ast.Symbol("error"): _error,
    ast.Symbol("#t"): True,
    ast.Symbol("#f"): False,
    ast.Symbol("="): lambda a, b: a == b,
    ast.Symbol("-"): lambda a, b: a - b,
    ast.Symbol("+"): lambda a, b: a + b,
}
