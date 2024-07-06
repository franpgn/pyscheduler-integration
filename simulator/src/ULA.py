import sys
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, '..', '..'))
sys.path.append(project_root)

from simulator.src.stack import Stack

class ULA:
    def __init__(self, size):
        self.stack = Stack(size)

        self.available_instructions = {
            11: "UNARY_NEGATIVE",
            12: "UNARY_NOT",
            15: "UNARY_INVERT",
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
            0: lambda x, y: y in x,
            1: lambda x, y: y not in x,
        }

    def UNARY_NEGATIVE(self):
        tos = self.stack.POP_TOP()
        self.stack.PUSH(-tos)

    def UNARY_NOT(self):
        tos = self.stack.POP_TOP()
        self.stack.PUSH(not tos)

    def UNARY_INVERT(self):
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

        result = self.available_bin_operators[operator](lhs, rhs)
        self.stack.PUSH(result)

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

        result = self.available_contains_operators[operator](lhs, rhs)
        self.stack.PUSH(result)
