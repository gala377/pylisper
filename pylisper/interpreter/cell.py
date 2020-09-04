from __future__ import annotations


class Cell:
    def __init__(self, car, cdr=None):
        self.car = car
        self.cdr = cdr

    def __iter__(self):
        return CellIterator(self)


class CellIterator:
    def __init__(self, cell: Cell):
        self._cell = cell

    def __iter__(self):
        return self

    def __next__(self):
        if self._cell is None:
            raise StopIteration
        val = self._cell.car
        self._cell = self._cell.cdr
        return val
