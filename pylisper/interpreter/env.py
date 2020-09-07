"""
Contains definition of the evaluation runtime environment
as well as standard runtime environment with implementations.
"""

from __future__ import annotations

from collections import UserDict
from typing import Mapping, Optional

from pylisper import ast
from pylisper.interpreter import objects as obj
from pylisper.interpreter.exceptions import EvaluationError


class Env(UserDict):
    """
    Runtime environment providing simple symbol lookkup.

    Environment is implemented as a simple wrapper around
    pythons `dict` class with ability to lookup values
    higher in the environments stack.

    Environments stack is provided by simply setting
    `parent` attribute to the higher environment.
    It is important to note that setting environments
    `parent` to itself will create a reference cycle.
    """

    def __init__(self, init: Optional[Mapping] = None, parent: Optional[Env] = None):
        """
        Creates a new environment.

        Args/Kwargs:
            `init`:
                Optional `dict` to initialize environment with.
            `parent`:
                Optional environments parent environment. If value cannot
                be found in this envirinment it will be then searched
                in its parent.
        """
        super().__init__(init)
        self.parent = parent

    @property
    def is_global(self) -> bool:
        """
        Checks if the environment is global.

        A global environment is considered to not have
        a parent.
        """
        return self.parent is None

    def lookup(self, sym: ast.Symbol) -> Optional[Env]:
        """
        Returns environment containing passed symbol or `None`.

        Args/Kwargs:
            `sym`:
                Symbol to search for.

        If current environment contains passed symbol then `self`
        is returned. Otherwise lookup is made in its paren environment.
        If the environment doesn't contain passed symbol and
        is global (which means it doesn't have a parent)
        then `None` is returned.
        """
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
"""
A `dict` instance containing standard environment to init
global environment with.
"""
