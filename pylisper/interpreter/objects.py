from typing import Sequence

from pylisper import ast

LambdaArgs = Sequence[ast.BaseNode]


class Lambda:
    def __init__(self, eval, body: ast.BaseNode, args: LambdaArgs):
        self._eval_visitor = eval
        self._body = body
        self._func_args = args
        self._def_env = eval._current_env

    def __call__(self, *args: ast.BaseNode):
        if len(self._func_args) != len(args):
            raise EvaluationError(
                f"number of call arguments doesn't match"
                f" expected {len(self._func_args)} got {len(args)}"
            )
        env_init = dict(zip(self._func_args, args))
        env = Env(env_init)
        # TODO: Make push-pop a context manager
        self._eval_visitor.push_env(self._def_env)
        self._eval_visitor.push_env(env)
        res = self._body.accept(self._eval_visitor)
        self._eval_visitor.pop_env()
        self._eval_visitor.pop_env()
        return res
