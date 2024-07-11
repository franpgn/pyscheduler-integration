import sys
import os
import time

from simulator.src.stack import Stack

script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, '..', '..'))
sys.path.append(project_root)


class ULA:
    def __init__(self, size):
        self.stack = Stack(size)

        self.available_instructions = {
            11: "UNARY_NEGATIVE",
            12: "UNARY_NOT",
            15: "UNARY_INVERT",
            25: "BINARY_SUBSCR",
            60: "STORE_SUBSCR",
            68: "GET_ITER",
            107: "COMPARE_OP",
            117: "IS_OP",
            118: "CONTAINS_OP",
            122: "BINARY_OP",
        }

        self.available_bin_operators = {
            0: lambda x, y: x + y,
            1: lambda x, y: x & y,
            2: lambda x, y: x // y,
            3: lambda x, y: x << y,
            5: lambda x, y: x * y,
            6: lambda x, y: x % y,
            7: lambda x, y: x | y,
            8: lambda x, y: x ** y,
            9: lambda x, y: x >> y,
            10: lambda x, y: x - y,
            11: lambda x, y: x / y,
            12: lambda x, y: x ^ y,
        }

        self.available_cmp_operators = {
            2: lambda x, y: x < y,
            26: lambda x, y: x <= y,
            40: lambda x, y: x == y,
            55: lambda x, y: x != y,
            68: lambda x, y: x > y,
            92: lambda x, y: x >= y,
        }

        self.available_identity_operators = {
            0: lambda x, y: x is y,
            1: lambda x, y: x is not y,
        }

        self.available_contains_operators = {
            0: lambda x, y: x in y,
            1: lambda x, y: x not in y,
        }

    @staticmethod
    def SLEEP_TIME(opcode):
        sleep_times = {
            1: 0.025,
            4: 0.04,
            5: 0.04,
            9: 0.005,
            11: 0.025,
            12: 0.025,
            15: 0.025,
            68: 0.035,
            83: 0.03,
            93: 0.04,
            99: 0.025,
            100: 0.025,
            102: 0.035,
            103: 0.035,
            104: 0.035,
            106: 0.03,
            107: 0.035,
            110: 0.03,
            114: 0.03,
            115: 0.03,
            116: 0.03,
            117: 0.025,
            118: 0.03,
            120: 0.025,
            121: 0.025,
            122: 0.035,
            124: 0.025,
            125: 0.025,
            126: 0.025,
            128: 0.03,
            129: 0.03,
            133: 0.035,
            134: 0.035,
            140: 0.035,
            150: 0.04,
            151: 0.035,
            157: 0.04,
            162: 0.04,
            163: 0.04,
            260: 0.03,
            261: 0.03
        }

        sleep_time = sleep_times.get(opcode, 0.1)
        time.sleep(sleep_time)

    def UNARY_NEGATIVE(self):
        if self.stack.top < 0:
            print("STACK UNDERFLOW -- NOT ENOUGH ELEMENTS")
            return
        tos = self.stack.POP_TOP()
        self.stack.PUSH(-tos)

    def UNARY_NOT(self):
        if self.stack.top < 0:
            print("STACK UNDERFLOW -- NOT ENOUGH ELEMENTS")
            return
        tos = self.stack.POP_TOP()
        self.stack.PUSH(not tos)

    def UNARY_INVERT(self):
        if self.stack.top < 0:
            print("STACK UNDERFLOW -- NOT ENOUGH ELEMENTS")
            return
        tos = self.stack.POP_TOP()
        self.stack.PUSH(~tos)

    def BINARY_OP(self, operator):
        if self.stack.top < 1:
            print("STACK UNDERFLOW -- NOT ENOUGH ELEMENTS")
            return

        if operator not in self.available_bin_operators:
            print("INVALID OPERATOR")
            return

        rhs = self.stack.POP_TOP()
        lhs = self.stack.POP_TOP()

        if isinstance(lhs, str) and lhs.isdigit():
            lhs = int(lhs)
        if isinstance(rhs, str) and rhs.isdigit():
            rhs = int(rhs)

        result = self.available_bin_operators[operator](lhs, rhs)
        self.stack.PUSH(result)


    def BINARY_SUBSCR(self):
        if self.stack.top < 1:
            print("STACK UNDERFLOW -- NOT ENOUGH ELEMENTS")
            return
        index = self.stack.POP_TOP()
        container = self.stack.POP_TOP()
        try:
            value = container[index]
            self.stack.PUSH(value)
        except (IndexError, TypeError) as e:
            print(f"SUBSCRIPT ERROR: {e}")

    def COMPARE_OP(self, operator):
        if self.stack.top < 1:
            print("STACK UNDERFLOW -- NOT ENOUGH ELEMENTS")
            return

        if operator not in self.available_cmp_operators:
            print("INVALID OPERATOR")
            return

        rhs = self.stack.POP_TOP()
        lhs = self.stack.POP_TOP()

        result = self.available_cmp_operators[operator](lhs, rhs)
        self.stack.PUSH(result)

    def IS_OP(self, operator):
        if self.stack.top < 1:
            print("STACK UNDERFLOW -- NOT ENOUGH ELEMENTS")
            return

        if operator not in self.available_identity_operators:
            print("INVALID OPERATOR")
            return

        rhs = self.stack.POP_TOP()
        lhs = self.stack.POP_TOP()

        result = self.available_identity_operators[operator](lhs, rhs)
        self.stack.PUSH(result)

    def CONTAINS_OP(self, operator):
        if self.stack.top < 1:
            print("STACK UNDERFLOW -- NOT ENOUGH ELEMENTS")
            return

        if operator not in self.available_contains_operators:
            print("INVALID OPERATOR")
            return

        rhs = self.stack.POP_TOP()
        lhs = self.stack.POP_TOP()

        if lhs is None:
            print("CONTAINS_OP ERROR: lhs is None")
            self.stack.PUSH(False)
            return

        result = self.available_contains_operators[operator](lhs, rhs)
        self.stack.PUSH(result)

    def STORE_SUBSCR(self):
        if self.stack.top < 2:
            print("STACK UNDERFLOW -- NOT ENOUGH ELEMENTS")
            return
        value = self.stack.POP_TOP()
        index = self.stack.POP_TOP()
        container = self.stack.POP_TOP()
        try:
            container[index] = value
        except (IndexError, TypeError) as e:
            print(f"STORE ERROR: {e}")

    def GET_ITER(self):
        try:
            self.stack.PUSH(iter(self.stack.POP_TOP()))
        except TypeError as e:
            print(f"Erro ao obter iterador: {e}")
            self.stack.PUSH(None)
