from collections import UserDict
from typing import Mapping, Optional

from pylisper.ast import NodeVisitor


class Env(UserDict):
    def __init__(init: Optional[Mapping] = None, parent: Optional[Env] = None):
        super().__init__(init)
        self.parent = parent

    @property
    def is_global(self):
        return self.parent is None


class AstWalkEvaluator(NodeVisitor):
    pass
