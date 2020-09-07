"""
Module containing exeptions that can happend during
evaluation.

Each exception derives from `EvaluationError` which
is equivalent to the `Exception` class
"""


class EvaluationError(Exception):
    """
    An exception to be raised during expression
    evaluation.
    """


class EvalTypeError(EvaluationError):
    """
    Exception to be thrown in case of mismatching types.
    """


class LogicError(EvaluationError):
    """
    Exception to be thrown in cases of situations that don't
    make logical sense.
    """


class InvalidFormError(EvaluationError):
    """
    Exception to be thrown in case of invalid from usage.
    """
