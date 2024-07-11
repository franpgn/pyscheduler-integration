import sys
import os
from apps.src.disassemble import disassemble

script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, '..', '..'))
sys.path.append(project_root)


def sum():
    a = 1
    b = 2
    c = 3
    d = 4
    e = 5
    f = 6
    g = 7
    h = a + b + c + d + e + f + g
    return h


disassemble(sum)
