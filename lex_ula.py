# Copyright 2015 [Brian Mc George]

import ply.ply.lex as lex

# Ula tokens
tokens = ('ID', 'FLOAT_LITERAL', 'WHITESPACE', 'COMMENT', 'AT', 'DOLLAR',
          'HASH', 'AND', 'EQUALS', 'OPEN_PARENTHESIS', 'CLOSE_PARENTHESIS')

# Regex
t_ID = r'[a-zA-Z_][a-zA-Z_0-9]*'
t_AT = r'\@'
t_DOLLAR = r'\$'
t_HASH = r'\#'
t_AND = r'\&'
t_EQUALS = r'\='
t_OPEN_PARENTHESIS = r'\('
t_CLOSE_PARENTHESIS = r'\)'
t_WHITESPACE = r'\s'
t_COMMENT = r'\/\*[\S\s]*\*\/|\/\/.*'


def t_FLOAT_LITERAL(t):
    r'([\+|-]?[0-9]+\.?[0-9]*([E|e][0-9]+)?)'
    t.value = float(t.value)
    return t


# Handle errors
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


# Build lexer
lexer = lex.lex()

test_data = '''
// Hello This is a comment
'''

lexer.input(test_data)

while True:
    tok = lexer.token()
    if not tok:
        break
    print(tok)
