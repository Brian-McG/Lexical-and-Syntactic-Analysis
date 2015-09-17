# Copyright 2015 [Brian Mc George]

import run_ula
import lex_command_arguments as args_

assembly_code = None

def emit_assembly_code(target_machine, module):
    return target_machine.emit_assembly(module)

def main():
    global assembly_code
    args = args_.manage_arguments()
    input_location = args.file_location[0]
    output_location = input_location.partition('.')[0]
    output_filename = output_location.split('/')[-1]
    run_ula.main()
    assembly_code = emit_assembly_code(run_ula.target_machine, run_ula.module)
    if (__name__ == "__main__"):
        output_location = output_filename + '.asm'
        with open(output_location, 'w') as file_writer:
            file_writer.write(str(assembly_code) + '\n')
        print(str(assembly_code))

if(__name__ == "__main__"):
    main()
