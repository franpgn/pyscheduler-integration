import dis
import re
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

    reduced_instructions = [(instr.opcode, instr.arg) for instr in instructions]

    print(instructions)

    with open("load.txt", "w") as f:
        f.write(f"STACK SIZE|{stack_size}\n")
        f.write(f"CONSTANTS|{constant_values}\n")
        f.write(f"LOCALS|{variable_values}\n")
        f.write(f"INSTRUCTIONS|{reduced_instructions}\n")

    return instructions