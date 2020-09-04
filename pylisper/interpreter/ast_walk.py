from __future__ import annotations

from typing import Sequence

from pylisper import ast
from pylisper.interpreter.objects import Lambda


class EvaluationError(Exception):
    """
    An exception to be raised during expression
    evaluation.
    """


class AstWalkEvaluator(ast.NodeVisitor):
    def __init__(self, env: Env):
        self._current_env = env
        self._special_forms = {
            ast.Symbol("define"): self._eval_define,
            ast.Symbol("quote"): self._eval_quote,
            ast.Symbol("cond"): self._eval_cond,
            ast.Symbol("lambda"): self._eval_lambda,
            # ast.Symbol("defun"): self._eval_defun,
            # ast.Symbol('set!'): self._eval_set,
        }

    def eval(self, ast: ast.BaseNode):
        return ast.accept(self)

    def visit_number(self, node: ast.Number):
        return node.value

    def visit_string(self, node: ast.String):
        return node.value

    def visit_symbol(self, node: ast.Symbol):
        env = self._current_env.lookup(node)
        if env is None:
            raise EvaluationError("Undefinied symbol")
        return env[node]

    def visit_list(self, node: ast.List):
        if not node:
            raise EvaluationError("Cannot evaluate an empty list")
        print(f"eval list - head is {node[0]}")
        if node[0] in self._special_forms:
            return self._special_forms[node[0]](node)
        evaled = [n.accept(self) for n in node]
        func = evaled.pop(0)
        if not callable(func):
            raise EvaluationError(
                "First value of an unquoted list should be a function"
            )
        return func(*evaled)

    def push_env(self, env: Env):
        env.parent = self._current_env
        self._current_env = env

    def pop_env(self):
        assert not self._current_env.is_global
        self._current_env = self._current_env.parent

    def _eval_lambda(self, node: ast.List):
        if len(node) != 3 or not isinstance(node[1], ast.List):
            raise EvaluationError(
                "lambda form should consist of arguments and a function body"
            )
        for arg in node[1]:
            if not isinstance(arg, ast.Symbol):
                raise EvaluationError("lambda forms arguments should be symbols")
        return Lambda(self, node[2], node[1])

    def _eval_cond(self, node: ast.List):
        exprs = node.exprs
        if len(exprs) < 3:
            raise EvaluationError(
                "cond form should consist of at least one condition"
                " and one expression to evaluate"
            )
        exprs = exprs[1:]
        while exprs:
            try:
                cond, expr, *exprs = exprs
            except ValueError:
                raise EvaluationError(
                    "each condition should be followed by"
                    " an expression to be evaluated."
                )
            if cond.accept(self):
                return expr.accept(self)
        return None

    def _eval_quote(self, node: ast.List):
        if len(node) != 2:
            raise EvaluationError(
                "quote form should consist of a single argument"
                " which is a value to be quoted"
            )
        return node[1]

    def _eval_defun(self, node: ast.List):
        ...

    def _eval_set(self, node: ast.List):
        ...

    def _eval_define(self, node: ast.List):
        exprs = node.exprs
        self._check_define_form(exprs)
        self._current_env[exprs[1]] = exprs[2].accept(self)

    def _check_define_form(self, exprs: Sequence[ast.BaseNode]):
        if len(exprs) != 3 or not isinstance(exprs[1], ast.Symbol):
            raise EvaluationError(
                "define form should consist of 2 elements"
                " first one being a symbol and the second one being"
                " an assigned expression"
            )
