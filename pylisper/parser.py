from rply import ParserGenerator

from pylisper.ast import *
from pylisper.lexer import (
    lexer,
    TOKENS,
)


ACCEPTED_TOKEN_NAMES = [t for t in TOKENS]

def _pylisper_parser_gen():
    pg = ParserGenerator(
        ACCEPTED_TOKEN_NAMES)

    @pg.production('sexpr : atom')
    @pg.production('sexpr : list')
    def list_sexpr(prod):
        return prod[0]

    @pg.production('list : LPAREN RPAREN')
    def empty_list(prod):
        return List()

    @pg.production('list : LPAREN sexprs RPAREN')
    def nonempty_list(prod):
        return List(prod[1].exprs)

    @pg.production('sexprs : sexprs sexpr')
    def multi_expr_sexprs(prod):
        return List(
            prod[0].exprs + [prod[1]])

    @pg.production('sexprs : sexpr')
    def single_expr_sexprs(prod):
        return List([prod[0]])

    @pg.production('atom : NUMBER')
    def atom_number(prod):
        return Number(int(prod[0].getstr()))

    @pg.production('atom : STRING')
    def atom_string(prod):
        return String(prod[0].getstr())

    @pg.production('atom : NAME')
    def atom_name(prod):
        return Symbol(prod[0].getstr())

    return pg

parser = _pylisper_parser_gen().build()
