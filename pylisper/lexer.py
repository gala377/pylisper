"""
Contains lexer as well as tokens definiton.

Whole module consists of 2 global variables;
    - `lexer` which is a lexer object ready to parse source line,
    - `TOKENS` dictionary mapping token names to their respoctive regexes.
"""

from rply import LexerGenerator

TOKENS = {
    "LPAREN": r"\(",
    "RPAREN": r"\)",
    "SYMBOL": r"""[^)('"`,;\s\r]+""",
    "UNKNOWN": r"""['"`,;]""",  # simple hack to get source pos of unknow char
}
"""
A `dict` containing token names with its
corresponding regexes.
"""


def _lispy_lexer_generator():
    """
    Creates a rply lexer generator.
    """
    lg = LexerGenerator()
    lg.ignore(r"\s+|(;;.*?(\n|$))")
    for name, pat in TOKENS.items():
        lg.add(name, pat)
    return lg


lexer = _lispy_lexer_generator().build()
