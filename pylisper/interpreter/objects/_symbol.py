from typing import Any

from pylisper.interpreter.objects._base import BaseObject


class Symbol(BaseObject):
    """
    Object representing an identifier in the source code.

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
        """
        Returns an instance of a `Symbol` class.

        Args/Kwargs:
            `value`:
                A string value representing a symbol.
            `*args`:
                Arguments to pass to `__new__`.
            `**kwargs`:
                Keyword arguments to pass to `__new__`.

        As described in class docstring.
        When calling this method with the symbol
        that it was already called with no new instance
        is created.
        """
        if value in cls._existing_symbols:
            return cls._existing_symbols[value]
        self = super().__new__(cls, *args, **kwargs)
        self.value = value
        cls._existing_symbols[value] = self
        return self

    def __str__(self):
        return self.value

    def __repr__(self):
        repr = super().__repr__()
        parts = repr.split()
        parts[0] = f"{parts[0]}({self.value})"
        return " ".join(parts)
