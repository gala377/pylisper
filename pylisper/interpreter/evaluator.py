import pylisper.interpreter.objects as obj
from pylisper.interpreter.env import Env
from pylisper.interpreter.exceptions import EvaluationError


class Evaluator:
    def __init__(self, env: Env):
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
        if isinstance(expr, obj.Number):
            res = self._eval_number(expr)
        elif isinstance(expr, obj.Symbol):
            res = self._eval_symbol(expr)
        else:
            res = self._eval_list(expr)
        return res

    def _eval_number(self, number: obj.Number):
        return number.value

    def _eval_symbol(self, symbol: obj.Symbol):
        env = self._current_env.lookup(symbol)
        if env is None:
            raise EvaluationError("Undefinied symbol")
        return env[symbol]

    def _eval_list(self, list: obj.Cell):
        if list is None:
            raise EvaluationError("Cannot evaluate an empty list")
        func, *args = list
        if isinstance(func, obj.Symbol) and func in self._special_forms:
            return self._special_forms[func](list)
        func = self.eval(func)
        args = [self.eval(arg) for arg in args]
        if not callable(func):
            raise EvaluationError(
                "First value of an unquoted list should be a function"
            )
        return func(*args)

    def push_env(self, env: Env):
        assert env is not self._current_env
        env.parent = self._current_env
        self._current_env = env

    def pop_env(self):
        assert not self._current_env.is_global
        self._current_env = self._current_env.parent

    def _eval_lambda(self, node: obj.Cell):
        try:
            _, args, body = node
        except ValueError:
            raise EvaluationError(
                "lambda form should consist of arguments and a function body"
            )
        if args is not None:
            if not isinstance(args, obj.Cell):
                raise EvaluationError("lambdas arguments should be a list")
            for arg in args:
                if not isinstance(arg, obj.Symbol):
                    raise EvaluationError("lambda form arguments should be symbols")
        return obj.Lambda(self, args, body)

    def _eval_cond(self, node: obj.Cell):
        try:
            _, *exprs = node
        except ValueError:
            raise EvaluationError(
                "cond form should consist of at least one condition"
                " and one expression to evaluate"
            )
        try:
            for cond, expr in exprs:
                if self.eval(cond):
                    return self.eval(expr)
        except (ValueError, TypeError):
            raise EvaluationError(
                "each condition should be followed by an expression to be evaluated."
            )
        return None

    def _eval_quote(self, node: obj.Cell):
        try:
            _, expr = node
        except ValueError:
            raise EvaluationError(
                "quote form should consist of a single argument"
                " which is a value to be quoted"
            )
        return expr

    def _eval_define(self, node: obj.Cell):
        try:
            _, sym, expr = node
        except ValueError:
            raise EvaluationError(
                "define form should consist of 2 elements"
                " first one being a symbol and the second one being"
                " an assigned expression"
            )
        if not isinstance(sym, obj.Symbol):
            raise EvaluationError(
                "first argument to the define form should be a symbol"
            )
        self._current_env[sym] = self.eval(expr)

    def _eval_set(self, node: obj.Cell):
        err = EvaluationError(
            "set! form should consist of memory reference (Symbol or cons cell)"
            " and an expression to evaluate"
        )
        try:
            _, ref, expr = node
        except ValueError:
            raise err
        if not isinstance(ref, obj.Symbol):
            raise err
        ref_env = self._current_env.lookup(ref)
        if ref_env is None:
            raise EvaluationError(f"unknown symbol {ref}")
        ref_env[ref] = self.eval(expr)

    def _eval_begin(self, node: obj.Cell):
        try:
            _, *exprs = node
        except ValueError:
            raise EvaluationError(
                "begin form should be followed by at least one expression"
            )
        for expr in exprs[:-1]:
            self.eval(expr)
        return self.eval(exprs[-1])
