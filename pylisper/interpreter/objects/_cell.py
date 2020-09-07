from __future__ import annotations

from typing import Any, Optional

from pylisper.interpreter.objects._base import BaseObject


class Cell(BaseObject):
    """
    `Cell` is a node in a singly-linked list.

    It is modeled after the original lisps list.
    Alias `car` for the underlaying value is provided.
    As well as static `cons` method that simply wraps
    the class constructor.

    `Cell` is an interator so it can be used with
    pattern matching to unpack values.


    Examples:

        >>> cell = Cell.cons("hello", Cell.cons(1, Cell.cons(2, None)))
        >>> fun, *args = cell
        >>> fun
        "hello"
        >>> args
        [1, 2]
        >>> head, middle, tail = cell
        >>> head
        "hello"
        >>> middle
        1
        >>> tail
        2
    """

    def __init__(self, value: Any, cdr: Optional[Cell] = None):
        """
        Creates a cell.

        Args/Kwargs:
            `value`:
                Value to hold in a cell.
            `cdr`:
                Optional rest of the list.
        """
        self.value = value
        self.cdr = cdr

    @property
    def car(self):
        """
        Simple getter for the `self.value`.
        """
        return self.value

    def __iter__(self):
        return CellIterator(self)

    @staticmethod
    def cons(value: Any, cell: Cell):
        """
        Simple wrapper for the constructor.
        """
        return Cell(value, cell)

    def __str__(self):
        body = " ".join(map(str, self))
        return f"({body})"


class CellIterator:
    """
    An iterator over the cells values.
    """
    def __init__(self, cell: Cell):
        self._cell = cell

    def __iter__(self):
        return self

    def __next__(self):
        if self._cell is None:
            raise StopIteration
        val = self._cell.value
        self._cell = self._cell.cdr
        return val
