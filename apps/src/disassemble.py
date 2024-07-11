import dis
import re
import sys
import os
from simulator.src.memory import Memory

script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, '..', '..'))
sys.path.append(project_root)


def disassemble(code):
    infos = dis.code_info(code)

    constants = re.search(r"Constants:\s*(.*?)(?=\n[A-Z]|\Z)", infos, re.DOTALL)

    if constants:
        constant_lines = constants.group(1).strip().split("\n")
        constant_values = [line.split(': ')[1].strip() for line in constant_lines]
        constant_values = [eval(value) for value in constant_values]
    else:
        constant_values = []

    variables = re.search(r"Variable names:\s*(.*?)(?=\n[A-Z]|\Z)", infos, re.DOTALL)

    if variables:
        variable_lines = variables.group(1).strip().split("\n")
        variable_values = [line.split(': ')[1].strip() for line in variable_lines]
    else:
        variable_values = []

    # Extrair nomes
    names = re.search(r"Names:\s*(.*?)(?=\n[A-Z]|\Z)", infos, re.DOTALL)
    if names:
        name_lines = names.group(1).strip().split("\n")
        name_values = [line.split(': ')[1].strip() for line in name_lines]
    else:
        name_values = []

    # Extrair tamanho da pilha
    stack_size_match = re.search(r"Stack size:\s*(\d+)", infos)
    stack_size = int(stack_size_match.group(1)) if stack_size_match else 0

    # Extrair instruções
    instructions = list(dis.get_instructions(code))
    processed = False
    reduced_instructions = {instruction.offset: [instruction.opcode, instruction.arg, instruction.argval, processed] for instruction in instructions}

    print(dis.dis(code))

    Memory.__init__()
    Memory.add_process({
        "pid": Memory.get_last_id(),
        "burst_time": 0,
        "priority": 1,
        "stack_size": int(stack_size),
        "constants": constant_values,
        "locals_var": variable_values,
        "instructions": reduced_instructions,
        "pc_total": list(reduced_instructions.keys())[-1]
    })
    json_data = Memory.get_process_queue()
    print(f'Novo processo na memoria: {json_data[-1]['id']}')
