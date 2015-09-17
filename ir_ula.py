# Copyright 2015 [Brian Mc George]

from llvmlite import ir
from ctypes import CFUNCTYPE, c_float
import llvmlite.binding as llvm
import errors_ula
import lex_command_arguments as args_

abstract_syntax_tree = None
last_var = None                 # Last variable assigned
var_dict = {}                   # Variable names with associated memory address
builder = None                  # create irbuilder to generate code


def generate_code(tree):
    global last_var
    global var_dict
    global builder
    if (tree[0] == "Start" or tree[0] == "Program"):
        for t in tree[1:]:
            generate_code(t)
    elif (tree[0] == "AssignStatement"):
        last_var = extract_value(tree[1])  # Variable name
        var_dict[last_var] = builder.alloca(ir.FloatType())
        builder.store(generate_code(tree[2]), var_dict[last_var])
    elif (tree[0] == "AddExpression"):
        return(builder.fadd(generate_code(tree[1]), generate_code(tree[2])))
    elif (tree[0] == "SubExpression"):
        return(builder.fsub(generate_code(tree[1]), generate_code(tree[2])))
    elif (tree[0] == "MulExpression"):
        var1 = generate_code(tree[1])
        var2 = generate_code(tree[2])
        return(builder.fmul(var1, var2))
    elif (tree[0] == "DivExpression"):
        return(builder.fdiv(generate_code(tree[1]), generate_code(tree[2])))
    elif (tree[0] == "IdentifierExpression"):
        return(builder.load(var_dict[extract_value(tree[1])]))
    elif (tree[0] == "FloatExpression"):
        return(ir.Constant(ir.FloatType(), float(extract_value(tree[1]))))


def main():
    global abstract_syntax_tree
    global builder
    args = args_.manage_arguments()
    input_location = args.file_location[0]
    output_location = input_location.partition('.')[0]
    output_filename = output_location.split('/')[-1]
    errors_ula.main()
    abstract_syntax_tree = errors_ula.result
    flttyp = ir.FloatType()  # create float type
    fnctyp = ir.FunctionType(flttyp, ())  # create function type to return a float
    module = ir.Module(name="ula")  # create module named "ula"
    func = ir.Function(module, fnctyp, name="main")  # create "main" function
    block = func.append_basic_block(name="entry")  # create block "entry" label
    builder = ir.IRBuilder(block)
    generate_code(abstract_syntax_tree)  # call code_gen() to traverse tree & generate code
    builder.ret(builder.load(var_dict[last_var]))  # specify return value
    if (__name__ == "__main__"):
        output_location = output_filename + '.ir'
        with open(output_location, 'w') as file_writer:
            file_writer.write(str(module) + '\n')
        print(str(module))
    return module


def extract_value(tree_value):
    return tree_value.split(',')[1]


if(__name__ == "__main__"):
    main()
