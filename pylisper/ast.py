from __future__ import annotations

from abc import ABC, abstractmethod
from collections import UserList
from typing import Any, Optional, Sequence


class BaseNode(ABC):
    """
    Base class for all of the AST nodes.

    Implementation consists of one abstact method
    `accept` that has to be implemented in the
    deriving classes in order to support visitor
    patter.

    Other than that this class doesn't impose
    any more requirements on the deriving classes.
    """

    @abstractmethod
    def accept(self, visitor: NodeVisitor):
        ...


class Number(BaseNode):
    def __init__(self, value: int):
        self.value = value

    def accept(self, visitor: NodeVisitor):
        return visitor.visit_number(self)

    def __str__(self):
        return str(self.value)


class Symbol(BaseNode):
    """
    AST node representing an identifier in the source code.

    `Symbol` is identified by the value it was created with.
    Two `Symbols` instances created with the same value
    will have the same mmemory address which means they
    can be compared with `is` operator.

    In order to provide this functionality `Symbol`
    class initializes instances on `__new__` instead
    of `__init__`. It keeps all of the already created
    instances in the internal storage `_existing_symbols`.
    Which is just a dictionary kept as a class atribute.
    If there already was an instance of a `Symbol` class
    created with the provided value then instead of creating
    a new instance the old one is returned.
    """

    _existing_symbols = {}

    def __new__(cls, value: str, *args: Any, **kwargs: Any):
        if value in cls._existing_symbols:
            return cls._existing_symbols[value]
        self = super().__new__(cls)
        self.value = value
        cls._existing_symbols[value] = self
        return self

    def accept(self, visitor: NodeVisitor):
        return visitor.visit_symbol(self)

    def __str__(self):
        return self.value

    def __repr__(self):
        repr = super().__repr__()
        parts = repr.split()
        parts[0] = f"{parts[0]}({self.value})"
        return " ".join(parts)


class List(UserList, BaseNode):
    def __init__(self, exprs: Optional[Sequence[BaseNode]] = None):
        super().__init__(exprs)

    @property
    def exprs(self):
        return self.data

    @property
    def empty(self):
        return len(self.data) == 0

    def accept(self, visitor: NodeVisitor):
        return visitor.visit_list(self)

    def __str__(self):
        inner = map(str, self.data)
        return f"({' '.join(inner)})"


class NodeVisitor(ABC):
    """
    NodeVisitor is an abstract interface for the
    classes that are willing to traverse
    an AST constructed from the `BaseNode` deriving
    objects.

    It provides one method per concrete ast node class
    (which means every node class which instances can
    be expected. So every node except the `BaseNode`).
    """

    @abstractmethod
    def visit_number(self, node: Number):
        ...

    @abstractmethod
    def visit_symbol(self, node: Symbol):
        ...

    @abstractmethod
    def visit_list(self, node: List):
        ...
