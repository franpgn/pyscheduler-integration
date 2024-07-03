import dis
import re
import sys
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, '..', '..'))
sys.path.append(project_root)

from simulator.src.memory import Memory

def disassemble(code):
    infos = dis.code_info(code)

    constants = re.search(r"Constants:\s*(.*?)(?=\n[A-Z]|\Z)", infos, re.DOTALL)

    if constants:
        constant_lines = constants.group(1).strip().split("\n")
        constant_values = [line.split(': ')[1] for line in constant_lines]
        constant_values = [eval(value) for value in constant_values]
    else:
        constant_values = []

    variables = re.search(r"Variable names:\s*(.*?)(?=\n[A-Z]|\Z)", infos, re.DOTALL)

    if variables:
        variable_lines = variables.group(1).strip().split("\n")
        variable_values = [line.split(': ')[1] for line in variable_lines]
    else:
        variable_values = []

    stack_size = re.search(r"Stack size:\s*(\d+)", infos).group(1)

    instructions = list(dis.get_instructions(code))
    processed = False
    reduced_instructions = [(instr.opcode, instr.arg, processed) for instr in instructions]

    Memory.__init__()
    Memory.add_process({
        "pid": Memory.get_last_id(),
        "burst_time": 0,
        "priority": 1,
        "stack_size": stack_size,
        "constants": constant_values,
        "local_vars": variable_values,
        "instructions": reduced_instructions
    }
    )
    json_data = Memory.get_process_queue()
    print(f'New process on memory: {json_data[-1]['pid']}')

