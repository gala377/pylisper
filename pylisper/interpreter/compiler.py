"""
Module contains simple compiler class
for the AST.
"""
import pylisper.interpreter.objects as obj
from pylisper import ast


class ObjectCompiler(ast.NodeVisitor):
    """
    Compiles AST to its corresponding object representation.

    `Symbol` and `Number` are translated without much changes.
    `List` nodes are transforem into singly linked list to
    better model original lisps memory model.
    """

    def visit_list(self, node: ast.List):
        cell = None
        for n in reversed(node):
            val = n.accept(self)
            cell = obj.Cell.cons(val, cell)
        return cell

    def visit_number(self, node: ast.Number):
        return obj.Number(node.value)

    def visit_symbol(self, node: ast.Symbol):
        return obj.Symbol(node.value)
