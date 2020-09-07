"""
Contains definition of the evaluation runtime environment
as well as standard runtime environment with implementations.
"""

from __future__ import annotations

from collections import UserDict
from typing import Mapping, Optional

from pylisper.interpreter.objects._symbol import Symbol


class Env(UserDict):
    """
    Runtime environment providing simple symbol lookkup.

    Environment is implemented as a simple wrapper around
    pythons `dict` class with ability to lookup values
    higher in the environments stack.

    Environments stack is provided by simply setting
    `parent` attribute to the higher environment.
    It is important to note that setting environments
    `parent` to itself will create a reference cycle.
    """

    def __init__(self, init: Optional[Mapping] = None, parent: Optional[Env] = None):
        """
        Creates a new environment.

        Args/Kwargs:
            `init`:
                Optional `dict` to initialize environment with.
            `parent`:
                Optional environments parent environment. If value cannot
                be found in this envirinment it will be then searched
                in its parent.
        """
        super().__init__(init)
        self.parent = parent

    @property
    def is_global(self) -> bool:
        """
        Checks if the environment is global.

        A global environment is considered to not have
        a parent.
        """
        return self.parent is None

    def lookup(self, sym: Symbol) -> Optional[Env]:
        """
        Returns environment containing passed symbol or `None`.

        Args/Kwargs:
            `sym`:
                Symbol to search for.

        If current environment contains passed symbol then `self`
        is returned. Otherwise lookup is made in its paren environment.
        If the environment doesn't contain passed symbol and
        is global (which means it doesn't have a parent)
        then `None` is returned.
        """
        assert isinstance(sym, Symbol)
        if sym in self.data:
            return self
        return None if self.parent is None else self.parent.lookup(sym)

    def __repr__(self):
        r = repr(self.data)
        if self.parent is not None:
            r = f"{r} => {repr(self.parent)}"
        return
