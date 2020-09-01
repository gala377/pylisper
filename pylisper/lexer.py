from rply import LexerGenerator


TOKENS = {
    'NUMBER': r'(0|\d+)',
    'LPAREN': r'\(',
    'RPAREN': r'\)',
    'STRING': r'".*?"',
    'NAME': r'[^\d\s")(][^\s)("]*',
}

def _lispy_lexer_generator():
    lg = LexerGenerator()
    lg.ignore(r'\s+')
    for name, pat in TOKENS.items():
        lg.add(name, pat)
    return lg

lexer = _lispy_lexer_generator().build()
