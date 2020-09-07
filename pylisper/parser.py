"""
Module containing `parser` object ready to parse source
when provided with a lexer and parsing exceptions.
"""
from rply import ParserGenerator

from pylisper.ast import List, Number, Symbol
from pylisper.lexer import TOKENS

ACCEPTED_TOKEN_NAMES = [t for t in TOKENS]


class IncompleteInput(Exception):
    """
    An exception to be thrown in case of possibility that
    the input might be incomplete.
    """


class UnexpectedCharacter(Exception):
    """
    An exception to be thrown in case of encountering
    an unexpected character in the input stream.
    """

    def __init__(self, char, line, column):
        super().__init__()
        self.char = char
        self.line = line
        self.column = column
        self.msg = f"Unexpected character ({line}:{column}): '{char}'"

    def __str__(self):
        return self.msg


def _pylisper_parser_gen():
    """
    Createas a rply parser generator for the pylisper.
    """
    pg = ParserGenerator(ACCEPTED_TOKEN_NAMES)

    @pg.production("sexpr : atom")
    @pg.production("sexpr : list")
    def list_sexpr(prod):
        return prod[0]

    @pg.production("list : LPAREN RPAREN")
    def empty_list(prod):
        return List()

    @pg.production("list : LPAREN sexprs RPAREN")
    def nonempty_list(prod):
        return List(prod[1].exprs)

    @pg.production("sexprs : sexprs sexpr")
    def multi_expr_sexprs(prod):
        return List(prod[0].exprs + [prod[1]])

    @pg.production("sexprs : sexpr")
    def single_expr_sexprs(prod):
        return List([prod[0]])

    @pg.production("atom : SYMBOL")
    def atom_symbol(prod):
        try:
            val = int(prod[0].getstr())
            return Number(val)
        except ValueError:
            return Symbol(prod[0].getstr())

    @pg.error
    def error_handler(tok):
        if tok.name == "$end":
            raise IncompleteInput
        # TODO: remove later
        raise UnexpectedCharacter(
            tok.value, tok.getsourcepos().lineno, tok.getsourcepos().colno
        )

    return pg


parser = _pylisper_parser_gen().build()
