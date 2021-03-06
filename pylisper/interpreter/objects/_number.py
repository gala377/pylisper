from __future__ import annotations

from pylisper.interpreter.objects._base import BaseObject


class Number(BaseObject):
    """
    Simple wrapper for a pythons integer.
    """

    def __init__(self, value: int):
        """
        Creates a new `Number`

        Args/Kwargs:
            value:
                Integer to wrap.
        """
        self.value = value

    def __str__(self):
        return str(self.value)

    def __eq__(self, other: Number):
        if not isinstance(other, Number):
            raise TypeError("Number class can only be compared with itself")
        return self.value == other.value

    def __add__(self, other: Number):
        if not isinstance(other, Number):
            raise TypeError("Number class can only be added with itself")
        return Number(self.value + other.value)

    def __sub__(self, other: Number):
        if not isinstance(other, Number):
            raise TypeError("Number class can only be added with itself")
        return Number(self.value - other.value)
