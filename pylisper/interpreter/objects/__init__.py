"""
This module contains classes for the object model
of the executed code.
    - `BaseObject` as a base class for all of the objects,
    - `Cell` representing a node in a singly-linked list,
    - `Number` being a simple wrapper for integer,
    - `Lambda`, a function capturing its environment;
    - `Symbol`, an identifier.
"""
from pylisper.interpreter.objects._base import BaseObject
from pylisper.interpreter.objects._cell import Cell
from pylisper.interpreter.objects._lambda import Lambda
from pylisper.interpreter.objects._number import Number
from pylisper.interpreter.objects._symbol import Symbol

__all__ = [
    "BaseObject",
    "Cell",
    "Number",
    "Lambda",
    "Symbol",
]
