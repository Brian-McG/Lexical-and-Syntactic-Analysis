# Copyright 2015 [Brian Mc George]

import os
import lex_command_arguments as args_
import ply.ply.lex as lex

# Constants
ID_CONST = 'ID'
FLOAT_LITERAL_CONST = 'FLOAT_LITERAL'
WHITESPACE_CONST = 'WHITESPACE'
COMMENT_CONST = 'COMMENT'
AT_CONST = 'AT'
DOLLAR_CONST = 'DOLLAR'
HASH_CONST = 'HASH'
AND_CONST = 'AND'
EQUALS_CONST = 'EQUALS'
OPEN_PARENTHESIS_CONST = 'OPEN_PARENTHESIS'
CLOSE_PARENTHESIS_CONST = 'CLOSE_PARENTHESIS'

# Ula tokens
tokens = (ID_CONST, FLOAT_LITERAL_CONST, WHITESPACE_CONST, COMMENT_CONST,
          AT_CONST, DOLLAR_CONST, HASH_CONST, AND_CONST, EQUALS_CONST,
          OPEN_PARENTHESIS_CONST, CLOSE_PARENTHESIS_CONST)

conversion_hash = {AT_CONST: '@', DOLLAR_CONST: '$',
                   HASH_CONST: '#', AND_CONST: '&',
                   EQUALS_CONST: '=',
                   OPEN_PARENTHESIS_CONST: '(',
                   CLOSE_PARENTHESIS_CONST: ')'}

# Regular Expressions
t_ID = r'[a-zA-Z_][a-zA-Z_0-9]*'
t_AT = r'\@'
t_DOLLAR = r'\$'
t_HASH = r'\#'
t_AND = r'\&'
t_EQUALS = r'\='
t_OPEN_PARENTHESIS = r'\('
t_CLOSE_PARENTHESIS = r'\)'
t_WHITESPACE = r'\s+'
t_COMMENT = r'\/\*[^(\*\/);]+\*\/|\/\/.*'
lexer = None


def t_FLOAT_LITERAL(t):
    r'([\+|-]?[0-9]+\.?[0-9]*([E|e][\+|\-]?[0-9]+)?)'
    return t


# Handle errors
def t_error(t):
    print("illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


def parse_input(input_data, output_file):
    # Build lexer
    lexer = lex.lex()
    # Pass in the input
    lexer.input(input_data)
    output_folder = 'output/'
    output_location = output_folder + output_file + '.tkn'
    os.makedirs(output_folder, exist_ok=True)
    with open(output_location, 'w') as file_writer:
        while (True):
            token = lexer.token()
            if (not token):
                break
            token_type = token.type
            if (token_type in conversion_hash):
                token_type = conversion_hash[token_type]
            if (token_type == ID_CONST or token_type == FLOAT_LITERAL_CONST):
                output = '{},{}'.format(token_type, token.value)
                print(output)
                file_writer.write(output+'\n')
            else:
                output = token_type
                print(output)
                file_writer.write(output+'\n')


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
