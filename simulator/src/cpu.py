import sys
import os
import json
import time

from simulator.src.ula import ULA
from pyscheduler.src.process import Process

script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, '..', '..'))
sys.path.append(project_root)


class CPU:
    def __init__(self, process: Process):

        self.constants = process.constants
        self.local_vars = process.local_vars
        self.stack_size = process.stack_size
        self.instructions = process.instructions
        self.pc = process.pc
        self.ULA = ULA(self.stack_size)

        self.available_instructions = {
            1: "POP_TOP",
            4: "END_FOR",
            5: "END_SEND",
            9: "NOP",
            11: "UNARY_NEGATIVE",
            12: "UNARY_NOT",
            15: "UNARY_INVERT",
            68: "GET_ITER",
            83: "RETURN_VALUE",
            93: "FOR_ITER",
            99: "SWAP",
            100: "LOAD_CONST",
            102: "BUILD_TUPLE",
            103: "BUILD_LIST",
            104: "BUILD_SET",
            106: "LOAD_ATTR",
            107: "COMPARE_OP",
            110: "JUMP_FORWARD",
            114: "POP_JUMP_IF_FALSE",
            115: "POP_JUMP_IF_TRUE",
            116: "LOAD_GLOBAL",
            117: "IS_OP",
            118: "CONTAINS_OP",
            120: "COPY",
            121: "RETURN_CONST",
            122: "BINARY_OP",
            124: "LOAD_FAST",
            125: "STORE_FAST",
            126: "DELETE_FAST",
            128: "POP_JUMP_IF_NOT_NONE",
            129: "POP_JUMP_IF_NONE",
            133: "BUILD_SLICE",
            134: "JUMP_BACKWARD_NO_INTERRUPT",
            140: "JUMP_BACKWARD",
            150: "YIELD_VALUE",
            151: "RESUME",
            157: "BUILD_STRING",
            162: "LIST_EXTEND",
            163: "SET_UPDATE",
            260: "JUMP",
            261: "JUMP_NO_INTERRUPT",
        }

        # opcode -> (function, has_argument)
        self.redirect = {
            1: (self.ULA.stack.POP_TOP, 0),
            4: (self.ULA.stack.END_FOR, 0),
            5: (self.ULA.stack.END_SEND, 0),
            9: (self.ULA.stack.NOP, 0),
            11: (self.ULA.UNARY_NEGATIVE, 0),
            12: (self.ULA.UNARY_NOT, 0),
            15: (self.ULA.UNARY_INVERT, 0),
            83: (self.ULA.stack.RETURN_VALUE, 0),
            99: (self.ULA.stack.SWAP, 1),
            100: (self.LOAD_CONST, 1),
            106: (self.LOAD_ATTR, 2),
            107: (self.ULA.COMPARE_OP, 1),
            110: (self.JUMP_FORWARD, 1),
            114: (self.POP_JUMP_IF_FALSE, 1),
            115: (self.POP_JUMP_IF_TRUE, 1),
            116: (self.LOAD_GLOBAL, 1),
            117: (self.ULA.IS_OP, 1),
            118: (self.ULA.CONTAINS_OP, 1),
            120: (self.ULA.stack.COPY, 1),
            121: (self.constants, 1),
            122: (self.ULA.BINARY_OP, 1),
            124: (self.LOAD_FAST, 1),
            125: (self.STORE_FAST, 1),
            126: (self.DELETE_FAST, 1),
            128: (self.POP_JUMP_IF_NOT_NONE, 1),
            129: (self.POP_JUMP_IF_NONE, 1),
            134: (self.JUMP_BACKWARD_NO_INTERRUPT, 1),
            140: (self.JUMP_BACKWARD, 1),
            151: (self.RESUME, 0),
            260: (self.JUMP, 1),
            261: (self.JUMP_NO_INTERRUPT, 1),
        }

    def SHOW_CPU(self):
        print("CPU:")

        print("INSTRUCTIONS:")
        for instr in self.instructions:
            instr_name = self.available_instructions.get(instr[0], instr[0])
            print(f"{instr_name} -> OPCODE {instr[0]} | ARGUMENT {instr[1]}")
        print()

        print(f"PC -> {self.pc}")
        print()

        print("MEMORY:")
        print(f"CONSTANTS -> {self.constants}")
        print(f"LOCALS -> {self.local_vars}")
        print()

        print("STACK:")
        self.ULA.stack.SHOW_STACK()

    def LOAD_CONST(self, index):
        self.ULA.stack.PUSH(self.constants[index])

    def LOAD_FAST(self, index):
        self.ULA.stack.PUSH(self.local_vars[index])

    def STORE_FAST(self, index):
        self.local_vars[index] = self.ULA.stack.POP_TOP()

    def DELETE_FAST(self, index):
        del self.local_vars[index]

    def JUMP_FORWARD(self, offset):
        self.pc += offset

    def JUMP_BACKWARD(self, offset):
        self.pc -= offset

    def JUMP_BACKWARD_NO_INTERRUPT(self, offset):
        self.pc -= offset

    def LOAD_GLOBAL(self, name):
        self.ULA.stack.PUSH(globals()[name])

    def LOAD_ATTR(self, obj, attr):
        self.ULA.stack.PUSH(getattr(self.ULA.stack.POP_TOP(), attr))

    def POP_JUMP_IF_TRUE(self, offset):
        if self.ULA.stack.POP_TOP():
            self.JUMP_FORWARD(offset)

    def POP_JUMP_IF_FALSE(self, offset):
        if not self.ULA.stack.POP_TOP():
            self.JUMP_FORWARD(offset)

    def POP_JUMP_IF_NOT_NONE(self, offset):
        if self.ULA.stack.POP_TOP() is not None:
            self.JUMP_FORWARD(offset)

    def POP_JUMP_IF_NONE(self, offset):
        if self.ULA.stack.POP_TOP() is None:
            self.JUMP_FORWARD(offset)

    def JUMP(self, offset):
        if offset < 0:
            self.JUMP_BACKWARD(-offset)
        else:
            self.JUMP_FORWARD(offset)

    def JUMP_NO_INTERRUPT(self, offset):
        if offset < 0:
            self.JUMP_BACKWARD(-offset)
        else:
            self.JUMP_FORWARD(offset)

    def RESUME(self):
        pass

    def RUN(self, process: Process, quantum):
        time_start = time.time()
        quantum /= 1000
        while not process.pc > len(process.instructions) and time_start + quantum > time.time():
            print("-" * 50)
            print()
            instruction = process.instructions[self.pc]
            opcode = instruction[0]
            argument = instruction[1]

            if opcode in self.redirect:
                function, has_argument = self.redirect[opcode]
                if has_argument:
                    function(argument)
                else:
                    function()
            else:
                print("INVALID OPCODE")
                break

            ULA.SLEEP_TIME(opcode)

            print("PC -> ", self.pc)
            instruction_name = self.available_instructions.get(opcode, opcode)
            print(f"{instruction_name} -> OPCODE {opcode} | ARGUMENT {argument}")
            print()

            print("MEMORY:")
            print(f"CONSTANTS -> {process.constants}")
            print(f"LOCALS -> {process.local_vars}")
            print()

            if opcode == 83:
                print("RETURN VALUE ->", self.ULA.stack.RETURN_VALUE())
                print()
                break
            elif opcode == 121:
                print("RETURN VALUE ->", process.constants[argument])
                print()
                break
            else:
                print("STACK:")
                self.ULA.stack.SHOW_STACK()
            print("-" * 50)
            self.pc += 1
            process.pc = self.pc
