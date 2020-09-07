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
