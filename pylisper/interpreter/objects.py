"""
Thsis module holds classes representing object model of
the evaluator.
"""
from __future__ import annotations

from typing import Sequence, Any

from pylisper import ast
from pylisper.interpreter.env import Env
from pylisper.interpreter.exceptions import EvaluationError

LambdaArgs = Sequence[ast.Symbol]


class Lambda:
    """
    Model representing a lambda function.

    Lambda is represented by its unevaluated body,
    list of arguments and environment captured at
    lambda definition.
    """
    def __init__(self, eval, body: ast.BaseNode, args: LambdaArgs):
        """
        Creates a lambda object.

        Args/Kwargs:
            `eval`:
                Evaluator, used to capture definition environment as well
                as to, later, evaluate lambdas body.
            `body`:
                Unevaluated function body.
            `args`:
                List of symbols to be later associated with values lambda was
                called with.
        """
        assert all(map(lambda x: isinstance(x, ast.Symbol), args))
        self._eval_visitor = eval
        self._body = body
        self._func_args = args
        self._def_env = eval._current_env
        if eval._current_env.is_global:
            self._def_env = None

    def __call__(self, *args: Any):
        """
        Evaluates lambdas body with passed arguments.

        Args/Kwarg:
            `*args`:
                Arguments to evaluate the body with.

        Evaluation is done by firstly pushing captured definition
        environment, then pushing environment created by
        associating values passed to the call with
        names provided during lambda definition; onto the
        environment stack and then evaluating the lambdas body.

        Environments are always popped from the stack even if
        exception happens during evaluation.

        If lambda was used to define a top-level function then
        it captures a global environment. In this case, on call,
        only arguments environment is pushed onto the stack
        as pushing a global one would create a reference cycle
        for the environments.
        """
        if len(self._func_args) != len(args):
            raise EvaluationError(
                f"number of call arguments doesn't match"
                f" expected {len(self._func_args)} got {len(args)}"
            )
        env_init = dict(zip(self._func_args, args))
        call_env = Env(env_init)
        self._push_envs(call_env)
        try:
            res = self._body.accept(self._eval_visitor)
        finally:
            self._pop_envs()
        return res

    def _push_envs(self, call_env):
        if self._def_env is not None:
            self._eval_visitor.push_env(self._def_env)
        self._eval_visitor.push_env(call_env)

    def _pop_envs(self):
        self._eval_visitor.pop_env()
        if self._def_env is not None:
            self._eval_visitor.pop_env()


class Cell:
    def __init__(self, car, cdr=None):
        self.car = car
        self.cdr = cdr

    def __iter__(self):
        return CellIterator(self)


class CellIterator:
    def __init__(self, cell: Cell):
        self._cell = cell

    def __iter__(self):
        return self

    def __next__(self):
        if self._cell is None:
            raise StopIteration
        val = self._cell.car
        self._cell = self._cell.cdr
        return val
