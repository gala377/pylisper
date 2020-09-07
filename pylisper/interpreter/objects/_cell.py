from __future__ import annotations

from typing import Any, Optional

from pylisper.interpreter.objects._base import BaseObject


class Cell(BaseObject):
    def __init__(self, value: Any, cdr: Optional[Cell] = None):
        self.value = value
        self.cdr = cdr

    @property
    def car(self):
        return self.value

    def __iter__(self):
        return CellIterator(self)

    @staticmethod
    def cons(value: Any, cell: Cell):
        return Cell(value, cell)

    def __str__(self):
        body = " ".join(map(str, self))
        return f"({body})"


class CellIterator:
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
