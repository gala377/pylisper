from __future__ import annotations

from collections import UserDict
from typing import Mapping, Optional

from pylisper import ast


class Env(UserDict):
    def __init__(self, init: Optional[Mapping] = None, parent: Optional[Env] = None):
        super().__init__(init)
        self.parent = parent

    @property
    def is_global(self) -> bool:
        return self.parent is None

    def lookup(self, sym: ast.Symbol) -> Env:
        assert isinstance(sym, ast.Symbol)
        if sym in self.data:
            return self
        return None if self.parent is None else self.parent.lookup(sym)
