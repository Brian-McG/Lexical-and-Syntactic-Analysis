# Copyright 2015 [Brian Mc George]

import os
import sys
import lex_ula
import parse_ula
import lex_command_arguments as args_

result = None
current_line_number = 0
assignment_set = set()


def apply_semantic_analysis(file_writer, abstract_syntax_tree):
        depth_first_search(result, file_writer)


def depth_first_search(output, file_writer, depth=0):
    index = 0
    global current_line_number
    global assigment_set
    if (isinstance(output, tuple)):
        for i in output:
            if (index == 0):
                if(i == 'AssignStatement'):
                    current_line_number += 1
                    split_up = output[1].split(',')
                    if (len(split_up) == 2 and split_up[0] == 'ID'):
                        if (split_up[1] in assignment_set):
                            output = 'semantic error on line {}'.format(current_line_number)
                            print(output)
                            if (file_writer is not None):
                                file_writer.write(output + '\n')
                            sys.exit()
                        else:
                            assignment_set.add(split_up[1])
                elif (i == 'IdentifierExpression'):
                    split_up = output[1].split(',')
                    if(len(split_up) == 2 and split_up[0] == 'ID'):
                        if (not(split_up[1] in assignment_set)):
                            output = 'semantic error on line {}'.format(current_line_number)
                            print(output)
                            if (file_writer is not None):
                                file_writer.write(output + '\n')
            else:
                depth_first_search(i, file_writer, depth + 1)
            index += 1


def main():
    global result
    args = args_.manage_arguments()
    input_location = args.file_location[0]
    output_location = input_location.partition('.')[0]
    output_filename = output_location.split('/')[-1]

    # When lexing, ignore all comments and whitespace
    lex_ula.t_ignore_WHITESPACE = r'\s+'
    lex_ula.t_ignore_COMMENT = r'\/\*[^(\*\/);]+\*\/|\/\/.*'
    lex_ula.t_WHITESPACE = r'a^'
    lex_ula.t_COMMENT = r'a^'
    if (__name__ == "__main__"):
        output_location = output_filename + '.err'
        with open(output_location, 'w') as file_writer:
            lex_ula.main(file_writer)
            result = parse_ula.main(file_writer)
            apply_semantic_analysis(file_writer, result)


if (__name__ == "__main__"):
    main()
