# Copyright 2015 [Brian Mc George]

import os
import ply.ply.yacc as yacc
import lex_command_arguments as args_
import lex_ula

# Workaround to whitespace issue - get confirmation on this issue!
lex_ula.t_ignore = ' '
lex_ula.main()

tokens = lex_ula.tokens


def p_start(p):
    '''start : program'''
    p[0] = ('Start', p[1])


def p_program(p):
    '''program : program statement
               | statement'''
    if(len(p) == 2 and p[1] is not None):
        p[0] = ('PROGRAM', p[1])
    elif(len(p) == 3 and p[1] is not None and p[2] is not None):
        print(p[2])
        p[0] = p[1] + (p[2],)
    elif(len(p) == 3 and p[1] is None and p[2] is not None):
        p[0] = ('PROGRAM', p[2])
    else:
        p[0] = p[1]


def p_comment(p):
    'statement : COMMENT'
    p[0] = None


def p_whitespace(p):
    'statement : WHITESPACE'
    p[0] = None


def p_whitespace_(p):
    'term : WHITESPACE'
    p[0] = None


def p_statement(p):
    '''statement : ID EQUALS expression'''
    p[0] = ('AssignStatement', 'ID,'+p[1], p[3])


def p_expression_at(p):
    'expression : expression AT term'
    p[0] = ('AddExpression', p[1], p[3])
    print('at: {}'.format(p[0]))

def p_expression_dollar(p):
    'expression : expression DOLLAR term'
    p[0] = ('SubExpression', p[1], p[3])
    print('dollar: {}'.format(p[0]))

def p_exression_term(p):
    'expression : term'
    p[0] = p[1]
    print('expressTerm: {}'.format(p[0]))

def p_term_hash(p):
    'term : term HASH factor'
    p[0] = ('MulExpression', p[1], p[3])
    print('hash: {}'.format(p[0]))


def p_term_and(p):
    'term : term AND factor'
    p[0] = ('DivExpression', p[1], p[3])
    print('and: {}'.format(p[0]))


def p_term_factor(p):
    'term : factor'
    p[0] = p[1]
    print('termFactor: {}'.format(p[0]))


def p_factor_expression(p):
    'factor : OPEN_PARENTHESIS expression CLOSE_PARENTHESIS'
    p[0] = (p[2])
    print('factorExpresS: {}'.format(p[0]))



def p_factor_float(p):
    'factor : FLOAT_LITERAL'
    p[0] = ('FloatExpression', 'FLOAT_LITERAL,'+p[1])
    print('floatExp: {}'.format(p[0]))


def p_factor_id(p):
    'factor : ID'
    p[0] = ('IdentifierExpression', 'ID,'+p[1])
    print('idExp: {}'.format(p[0]))


#def p_factor_whitespace(p):
#    '''factor : WHITESPACE'''
#    p[0] = None


#def p_factor_comment(p):
#    '''factor : COMMENT'''
#    p[0] = None

# Ignore if input cannot be matched
def p_error(p):
    print("Error:")
    print(p)
    None

def parse_input(input_data, output_file):
    # Build lexer
    parser = yacc.yacc()
    output_folder = 'output/'
    output_location = output_folder + output_file + '.ast'
    os.makedirs(output_folder, exist_ok=True)
    result = parser.parse(input_data)
    print(result)


def main():
    args = args_.manage_arguments()
    input_location = args.file_location[0]
    if os.path.isfile(input_location):
        with open(input_location, 'r') as file_reader:
            input_data = file_reader.read()
            output_location = input_location.partition('.')[0]
            output_filename = output_location.split('/')[-1]
            parse_input(input_data, output_filename)
    else:
        print("File " + input_location + " does not exist.")

if __name__ == "__main__":
    main()
