# Copyright 2015 [Brian Mc George]
from __future__ import print_function
from ctypes import CFUNCTYPE, c_float
import ir_ula
import llvmlite.binding as llvm
import lex_command_arguments as args_

llvm.initialize()
llvm.initialize_native_target()
llvm.initialize_native_asmprinter()

intermediary_code = None
engine = None
module = None
target_machine = None
result = None


def create_run_engine():
    global target_machine
    # Create target machine
    target = llvm.Target.from_default_triple()
    target_machine = target.create_target_machine()

    # Add run engine
    backing_mod = llvm.parse_assembly("")
    engine = llvm.create_mcjit_compiler(backing_mod, target_machine)
    return engine


def compile_intermediary_code(engine, intermediary_code):
    # Create an llvm module object from the intermediary code
    mod = llvm.parse_assembly(intermediary_code)
    mod.verify()

    # Add module to engine and prepair for execution
    engine.add_module(mod)
    engine.finalize_object()
    return mod


def main():
    global engine
    global module
    global intermediary_code
    global result
    args = args_.manage_arguments()
    input_location = args.file_location[0]
    output_location = input_location.partition('.')[0]
    output_filename = output_location.split('/')[-1]

    intermediary_code = str(ir_ula.main())
    engine = create_run_engine()
    module = compile_intermediary_code(engine, intermediary_code)

    # Find pointer to function to execute
    function_ptr = engine.get_function_address("main")

    # Execute the function using ctypes
    c_function = CFUNCTYPE(c_float)(function_ptr)
    result = c_function()
    if (__name__ == "__main__"):
        output_location = output_filename + '.run'
        with open(output_location, 'w') as file_writer:
            file_writer.write(str(result) + '\n')
        print(str(result))


if(__name__ == "__main__"):
    main()
