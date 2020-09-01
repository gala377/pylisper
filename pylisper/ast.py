from abc import (
    ABC,
    abstractmethod,
)

from rply.token import BaseBox


class BaseNode(ABC, BaseBox):

    @abstractmethod
    def accept(self, visitor): ...

class Number(BaseNode):
    def __init__(self, value):
        self.value = value

    def accept(self, visitor):
        visitor.visit_number(self)

class String(BaseNode):
    def __init__(self, value):
        self.value = value

    def accept(self, visitor):
        visitor.visit_string(self)

class Symbol(BaseNode):
    def __init__(self, value):
        self.value = value

    def accept(self, visitor):
        visitor.visit_symbol(self)

class List(BaseNode):
    def __init__(self, exprs=None):
        self.exprs = exprs

    def accept(self, visitor):
        visitor.visit_list(self)
