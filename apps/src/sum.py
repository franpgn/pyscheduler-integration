import sys
import os
from apps.src.disassemble import disassemble

script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, '..', '..'))
sys.path.append(project_root)


def sum():
    a = 1
    b = 2

    c = a + b
    return c


def sum_to_byte_code():
    disassemble(sum)
