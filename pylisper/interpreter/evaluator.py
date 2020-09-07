import pylisper.interpreter.objects as obj
from pylisper.interpreter.env import Env
from pylisper.interpreter.exceptions import (EvalTypeError, EvaluationError,
                                             InvalidFormError, LogicError)


class Evaluator:
    """
    Allows for continous evaluation of
    a model compiled by `ObjectCompiler`.
    """

    def __init__(self, env: Env):
        """
        Create new Evaluator.

        Args/Kwargs:
            `env`:
                Environment to initialize the Evaluator with.
        """
        self._current_env = env
        self._special_forms = {
            obj.Symbol("define"): self._eval_define,
            obj.Symbol("quote"): self._eval_quote,
            obj.Symbol("cond"): self._eval_cond,
            obj.Symbol("lambda"): self._eval_lambda,
            obj.Symbol("set!"): self._eval_set,
            obj.Symbol("begin"): self._eval_begin,
        }

    def eval(self, expr: obj.BaseObject):
        """
        Evaluate given expression with the environment
        passed during object creation.

        Args/Kwargs:
            `expr`:
                Expression to evaluate.

        Raises:
            `EvaluationError`:
                In case of error during evaluation.
        """
        while True:
            if isinstance(expr, obj.Number):
                res = self._eval_number(expr)
            elif isinstance(expr, obj.Symbol):
                res = self._eval_symbol(expr)
            else:
                res = self._eval_list(expr)
                if isinstance(res, _ReuseStack):
                    expr = res.expr
                    continue
            return res

    def _eval_number(self, number: obj.Number):
        return number.value

    def _eval_symbol(self, symbol: obj.Symbol):
        env = self._current_env.lookup(symbol)
        if env is None:
            raise EvaluationError(f"Undefinied symbol {symbol}")
        return env[symbol]

    def _eval_list(self, list: obj.Cell):
        if list is None:
            raise LogicError("Cannot evaluate an empty list")
        func, *args = list
        if isinstance(func, obj.Symbol) and func in self._special_forms:
            return self._special_forms[func](list)
        func = self.eval(func)
        args = [self.eval(arg) for arg in args]
        if not callable(func):
            raise InvalidFormError(
                "First value of an unquoted list should be a function"
            )
        return func(*args)

    def push_env(self, env: Env):
        """
        Pushes new environment onto the stack.

        Assertion is made to make sure that the same
        environment is not pushed twice as that would
        create a reference cycle. And probably that
        is not what you want anyway.
        """
        assert env is not self._current_env
        env.parent = self._current_env
        self._current_env = env

    def pop_env(self):
        """
        Pops environment from the stack.

        Assertion is made to make sure that top level
        environment is not popped from the stack as
        that is not something that should ever happen.
        """
        assert not self._current_env.is_global
        self._current_env = self._current_env.parent

    def _eval_lambda(self, node: obj.Cell):
        try:
            _, args, body = node
        except ValueError:
            raise InvalidFormError(
                "lambda form should consist of arguments and a function body"
            )
        if args is not None:
            if not isinstance(args, obj.Cell):
                raise InvalidFormError("lambdas arguments should be a list")
            for arg in args:
                if not isinstance(arg, obj.Symbol):
                    raise InvalidFormError("lambda form arguments should be symbols")
        return obj.Lambda(self, args, body)

    def _eval_cond(self, node: obj.Cell):
        try:
            _, *exprs = node
        except ValueError:
            raise InvalidFormError(
                "cond form should consist of at least one condition"
                " and one expression to evaluate"
            )
        try:
            for cond, expr in exprs:
                if self.eval(cond):
                    return _ReuseStack(expr)
        except (ValueError, TypeError):
            raise InvalidFormError(
                "each condition should be followed by an expression to be evaluated."
            )

    def _eval_quote(self, node: obj.Cell):
        try:
            _, expr = node
        except ValueError:
            raise InvalidFormError(
                "quote form should consist of a single argument"
                " which is a value to be quoted"
            )
        return expr

    def _eval_define(self, node: obj.Cell):
        try:
            _, sym, expr = node
        except ValueError:
            raise InvalidFormError(
                "define form should consist of 2 elements"
                " first one being a symbol and the second one being"
                " an assigned expression"
            )
        if not isinstance(sym, obj.Symbol):
            raise InvalidFormError(
                "first argument to the define form should be a symbol"
            )
        self._current_env[sym] = self.eval(expr)

    def _eval_set(self, node: obj.Cell):
        err = InvalidFormError(
            "set! form should consist of memory reference (Symbol or cons cell)"
            " and an expression to evaluate"
        )
        try:
            _, ref, expr = node
        except ValueError:
            raise err
        if isinstance(ref, obj.Symbol):
            ref_env = self._current_env.lookup(ref)
            if ref_env is None:
                raise EvaluationError(f"unknown symbol {ref}")
            ref_env[ref] = self.eval(expr)
        elif isinstance(ref, obj.Cell) and ref.car is obj.Symbol("car"):
            cell = self._eval_car_to_cell(ref)
            cell.value = self.eval(expr)
        else:
            raise err

    def _eval_car_to_cell(self, node: obj.Cell):
        try:
            car, expr = node
        except ValueError:
            raise InvalidFormError(
                "car should be followed by a single expression to evaluate"
            )
        cell = self.eval(expr)
        if cell is None:
            raise LogicError("car cannot be used on an empty list")
        if not isinstance(cell, obj.Cell):
            raise EvalTypeError("car can only be called on a list")
        return cell

    def _eval_begin(self, node: obj.Cell):
        try:
            _, *exprs = node
        except ValueError:
            raise InvalidFormError(
                "begin form should be followed by at least one expression"
            )
        for expr in exprs[:-1]:
            self.eval(expr)
        return _ReuseStack(exprs[-1])


class _ReuseStack:
    """
    Simple marker to wrap returned expression with if
    the evaluator should perform tail optimization.
    """

    def __init__(self, expr):
        self.expr = expr
