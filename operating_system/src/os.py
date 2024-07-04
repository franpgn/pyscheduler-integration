import sys
import os
from apps.src.TestCPU import my_function
from simulator.src.memory import Memory
from simulator.src.cpu import CPU

script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, '..', '..'))
sys.path.append(project_root)


def main():
    my_function()
    Memory.send_process_queue()
    Memory.start_scheduler()
    cpu = CPU()
    cpu.SHOW_CPU()
    cpu.RUN()
