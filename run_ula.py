# Copyright 2015 [Brian Mc George]
from __future__ import print_function
from ctypes import CFUNCTYPE, c_float
import ir_ula
import llvmlite.binding as llvm

llvm.initialize()
llvm.initialize_native_target()
llvm.initialize_native_asmprinter()

intermediary_code = None
engine = None
module = None


def create_run_engine():
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
    intermediary_code = ir_ula.main()
    engine = create_run_engine()
    module = compile_intermediary_code(engine, intermediary_code)

    # Find pointer to function to execute
    function_ptr = engine.get_function_address("main")

    # Execute the function using ctypes
    c_function = CFUNCTYPE(c_float)(func_ptr)
    result = c_function()
    print(result)


if(__name__ == "__main__"):
    main()
