import sys
import os
import json
import time

from simulator.src.ula import ULA
from pyscheduler.src.process import Process
import numpy as np
from scipy.ndimage import convolve
from collections.abc import Iterator

script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, '..', '..'))
sys.path.append(project_root)

builtin_functions = {
    'len': len,
    'range': range,
    'print': print,
}


class CPU:
    def __init__(self, process: Process):

        self.constants = process.constants
        self.local_vars = process.local_vars
        self.stack_size = process.stack_size
        self.instructions = process.instructions
        self.pc = process.pc
        self.names = process.names
        self.ULA = ULA(self.stack_size)

        self.available_instructions = {
            1: "POP_TOP",
            4: "END_FOR",
            5: "END_SEND",
            9: "NOP",
            11: "UNARY_NEGATIVE",
            12: "UNARY_NOT",
            15: "UNARY_INVERT",
            25: "BINARY_SUBSCR",
            60: "STORE_SUBSCR",
            68: "GET_ITER",
            83: "RETURN_VALUE",
            93: "FOR_ITER",
            99: "SWAP",
            100: "LOAD_CONST",
            102: "BUILD_TUPLE",
            103: "BUILD_LIST",
            104: "BUILD_SET",
            105: "BUILD_MAP",
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
            134: "JUMP_BACKWARD_NO_INTERRUPT",
            140: "JUMP_BACKWARD",
            150: "YIELD_VALUE",
            151: "RESUME",
            157: "BUILD_STRING",
            162: "LIST_EXTEND",
            163: "SET_UPDATE",
            171: "CALL",
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
            25: (self.ULA.BINARY_SUBSCR, 0),
            60: (self.ULA.STORE_SUBSCR, 0),
            68: (self.ULA.GET_ITER, 0),
            83: (self.ULA.stack.RETURN_VALUE, 0),
            93: (self.FOR_ITER, 1),
            99: (self.ULA.stack.SWAP, 1),
            100: (self.LOAD_CONST, 1),
            102: (self.BUILD_TUPLE, 1),
            103: (self.BUILD_LIST, 1),
            104: (self.BUILD_SET, 1),
            105: (self.BUILD_MAP, 1),
            106: (self.LOAD_ATTR, 1),
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
            157: (self.BUILD_STRING, 1),
            162: (self.LIST_EXTEND, 1),
            163: (self.SET_UPDATE, 1),
            171: (self.CALL, 1),
            260: (self.JUMP, 1),
            261: (self.JUMP_NO_INTERRUPT, 1),
        }

    def SHOW_CPU(self):
        print("CPU:")

        print("INSTRUCTIONS:")
        for instruction in self.instructions.values():
            instruction_name = self.available_instructions.get(instruction[0], instruction[0])
            print(f"{instruction_name} -> OPCODE {instruction[0]} | ARGUMENT {instruction[1]}")
        print()

        print(f"PC -> {self.pc}")
        print()

        print("MEMORY:")
        print(f"CONSTANTS -> {self.constants}")
        print(f"LOCALS -> {self.local_vars}")
        print(f"NAMES -> {self.names}")
        print()

        print("STACK:")
        self.ULA.stack.SHOW_STACK()

    def LOAD_CONST(self, index):
        self.ULA.stack.PUSH(self.constants[index])

    def LOAD_FAST(self, index):
        if index < len(self.local_vars):
            value = self.local_vars[index]
            if isinstance(value, str):
                if value.isdigit():
                    value = int(value)
                else:
                    value = 0
            self.ULA.stack.PUSH(value)
        else:
            print(f"INDEX ERROR: Invalid index {index} for locals.")
            self.ULA.stack.PUSH(None)

    def STORE_FAST(self, index):
        if index < len(self.local_vars):
            value = self.ULA.stack.POP_TOP()
            self.local_vars[index] = value
        else:
            print(f"INDEX ERROR: Invalid index {index} for locals.")

    def DELETE_FAST(self, index):
        del self.local_vars[index]

    def JUMP_FORWARD(self, offset):
        self.pc += offset + 1

    def JUMP_BACKWARD(self, offset):
        self.pc -= offset

    def JUMP_BACKWARD_NO_INTERRUPT(self, offset):
        self.pc -= offset

    def LOAD_GLOBAL(self, namei):
        index = namei >> 1
        global_name = self.names[index]

        if global_name == 'np':
            self.ULA.stack.PUSH(np)
        elif global_name == 'convolve':
            self.ULA.stack.PUSH(convolve)
        elif global_name in builtin_functions:
            self.ULA.stack.PUSH(builtin_functions[global_name])
        else:
            raise ValueError(f"Unsupported global name: {global_name}")

    def LOAD_ATTR(self, namei):
        index = namei >> 1
        attr_name = self.names[index]

        if not isinstance(attr_name, str):
            raise TypeError(f"attribute name must be string, not '{type(attr_name).__name__}'")

        obj = self.ULA.stack.POP_TOP()

        print(f"Tentando acessar o atributo '{attr_name}' do objeto: {obj}")

        if namei & 1:
            method = getattr(obj, attr_name, None)
            if method is not None and callable(method):
                self.ULA.stack.PUSH(obj)
                self.ULA.stack.PUSH(method)
            else:
                self.ULA.stack.PUSH(None)
                self.ULA.stack.PUSH(method)
        else:
            try:
                self.ULA.stack.PUSH(getattr(obj, attr_name))
            except AttributeError as e:
                print(f"Erro ao acessar atributo: {e}")
                self.ULA.stack.PUSH(None)

    def LIST_EXTEND(self, count):
        items = [self.ULA.stack.POP_TOP() for _ in range(count)]
        list_obj = self.ULA.stack.POP_TOP()
        list_obj.extend(items[::-1])
        self.ULA.stack.PUSH(list_obj)

    def BUILD_LIST(self, count):
        items = [self.ULA.stack.POP_TOP() for _ in range(count)]
        self.ULA.stack.PUSH(items[::-1])

    def BUILD_TUPLE(self, count):
        items = [self.ULA.stack.POP_TOP() for _ in range(count)]
        self.ULA.stack.PUSH(tuple(items[::-1]))

    def BUILD_SET(self, count):
        items = [self.ULA.stack.POP_TOP() for _ in range(count)]
        self.ULA.stack.PUSH(set(items))

    def BUILD_STRING(self, count):
        strings = [self.ULA.stack.POP_TOP() for _ in range(count)]
        self.ULA.stack.PUSH(''.join(strings[::-1]))

    def SET_UPDATE(self, count):
        items = [self.ULA.stack.POP_TOP() for _ in range(count)]
        set_obj = self.ULA.stack.POP_TOP()
        set_obj.update(items)
        self.ULA.stack.PUSH(set_obj)

    def RESUME(self):
        pass

    def POP_JUMP_IF_TRUE(self, offset):
        if self.ULA.stack.POP_TOP():
            self.JUMP_FORWARD(offset)
        else:
            self.JUMP_FORWARD(3)

    def POP_JUMP_IF_FALSE(self, offset):
        if not self.ULA.stack.POP_TOP():
            self.JUMP_FORWARD(offset)
        else:
            self.JUMP_FORWARD(3)

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

    def BUILD_MAP(self, count):
        items = {}
        for _ in range(count):
            value = self.ULA.stack.POP_TOP()
            key = self.ULA.stack.POP_TOP()
            items[key] = value
        self.ULA.stack.PUSH(items)

    def CALL(self, arg_count):
        args = [self.ULA.stack.POP_TOP() for _ in range(arg_count)]
        args.reverse()
        function = self.ULA.stack.POP_TOP()

        if callable(function):
            print(f"Chamando função {function.__name__} com argumentos: {args}")

            if function.__name__ == 'convolve':
                input_array, kernel = args
                input_array = np.asarray(input_array)
                kernel = np.asarray(kernel)

                if input_array.ndim != kernel.ndim:
                    if kernel.ndim < input_array.ndim:
                        kernel = kernel.reshape((1,) * (input_array.ndim - kernel.ndim) + kernel.shape)
                    elif input_array.ndim < kernel.ndim:
                        input_array = input_array.reshape((1,) * (kernel.ndim - input_array.ndim) + input_array.shape)

                print(f"Forma do input_array após ajuste: {input_array.shape}")
                print(f"Forma do kernel: {kernel.shape}")

                if kernel.ndim != input_array.ndim:
                    raise ValueError("Kernel deve ser um array da mesma dimensionalidade que o input_array")

                print(f"Forma final do input_array: {input_array.shape}")
                print(f"Forma final do kernel: {kernel.shape}")

            result = function(*args)
            print(f"Resultado da função: {result}")
        else:
            raise TypeError(f"Objeto {function} não é chamável.")

        self.ULA.stack.PUSH(result)

    def FOR_ITER(self, jump_offset):
        iterator = self.ULA.stack.POP_TOP()
        if isinstance(iterator, Iterator):
            try:
                item = next(iterator)
                self.ULA.stack.PUSH(item)
                self.ULA.stack.PUSH(iterator)
            except StopIteration:
                self.pc += jump_offset + 1
        else:
            raise TypeError("Objeto não é um iterador")

    def RUN(self, process: Process, quantum):
        time_start = time.time()
        quantum /= 1000
        while not process.pc >= process.total_pc:
            print("-" * 50)
            print()
            instruction = process.instructions[f"{self.pc}"]
            opcode = instruction[0]
            argument = instruction[1]
            argument_val = instruction[2]

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
            instr_name = self.available_instructions.get(opcode, opcode)
            print(f"{instr_name} -> OPCODE {opcode} | ARGUMENT {argument} | ARGUMENT_VALUE {argument_val}")
            print()

            print("MEMORY:")
            print(f"CONSTANTS -> {self.constants}")
            print(f"LOCALS -> {self.local_vars}")
            print(f"NAMES -> {self.names}")
            print()

            if opcode == 83:  # RETURN_VALUE
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
            if opcode not in [93, 107, 106, 116, 171, 25, 122, 150, 115, 140, 60]:
                self.pc += 2
            elif opcode in [93, 115]:  # FOR_ITER
                continue
            elif opcode == 171:
                self.pc += 8
            elif opcode == 116:
                self.pc += 10
            elif opcode == 106:
                self.pc += 20
            elif opcode == 140:  # JUMP_BACKWARD
                pass
            else:
                self.pc += 4
            process.pc = self.pc
