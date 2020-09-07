from __future__ import annotations

from typing import Any, Sequence

from pylisper.interpreter.env import Env
from pylisper.interpreter.exceptions import EvaluationError
from pylisper.interpreter.objects._base import BaseObject
from pylisper.interpreter.objects._symbol import Symbol

LambdaArgs = Sequence[Symbol]


class Lambda(BaseObject):
    """
    Model representing a lambda function.

    Lambda is represented by its unevaluated body,
    list of arguments and environment captured at
    lambda definition.
    """

    def __init__(self, eval, args: LambdaArgs, body: BaseObject):
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
        self._evaluator = eval
        self._body = body
        self._func_args = [] if args is None else args

        assert all(map(lambda x: isinstance(x, Symbol), self._func_args))

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
        func_args = [x for x in self._func_args]
        if len(func_args) != len(args):
            raise EvaluationError(
                f"number of call arguments doesn't match"
                f" expected {len(func_args)} got {len(args)}"
            )
        env_init = dict(zip(func_args, args))
        call_env = Env(env_init)
        self._push_envs(call_env)
        try:
            return self._evaluator.eval(self._body)
        finally:
            self._pop_envs()

    def _push_envs(self, call_env: Env):
        if self._def_env is not None:
            self._evaluator.push_env(self._def_env)
        self._evaluator.push_env(call_env)

    def _pop_envs(self):
        self._evaluator.pop_env()
        if self._def_env is not None:
            self._evaluator.pop_env()

    def __str__(self):
        return f"lambda {self.args} {self.body}"
