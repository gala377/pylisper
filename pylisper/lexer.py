from rply import LexerGenerator

TOKENS = {
    "LPAREN": r"\(",
    "RPAREN": r"\)",
    "STRING": r'"([^"\\]|\\.)*"',
    "SYMBOL": r"""[^)('"`,;\s]*""",
}


def _lispy_lexer_generator():
    lg = LexerGenerator()
    lg.ignore(r"\s+|(;.*?(\n|$))")
    for name, pat in TOKENS.items():
        lg.add(name, pat)
    return lg


lexer = _lispy_lexer_generator().build()
