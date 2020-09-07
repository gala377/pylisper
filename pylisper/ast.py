from __future__ import annotations

from abc import ABC, abstractmethod
from collections import UserList
from typing import Optional, Sequence


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
    """
    AST node representing a numerical value.

    Just a simple wrapper for the integer value inside
    with support for the Visitor protocol.
    """

    def __init__(self, value: int):
        self.value = value

    def accept(self, visitor: NodeVisitor):
        return visitor.visit_number(self)

    def __str__(self):
        return str(self.value)


class Symbol(BaseNode):
    """
    Simple wrapper for the string value representing
    an indentifier.
    """

    def __init__(self, value: str):
        self.value = value

    def accept(self, visitor: NodeVisitor):
        return visitor.visit_symbol(self)

    def __str__(self):
        return self.value


class List(UserList, BaseNode):
    """
    Wrapper for the list object holding all of the
    contained ast nodes.
    """

    def __init__(self, exprs: Optional[Sequence[BaseNode]] = None):
        """
        Initialiazes underlying list to the `exprs`.
        """
        super().__init__(exprs)

    @property
    def exprs(self):
        """
        Returns underalying list.
        """
        return self.data

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
