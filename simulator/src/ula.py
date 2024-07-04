import sys
import os
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
            107: "COMPARE_OP",
            117: "IS_OP",
            118: "CONTAINS_OP",
            122: "BINARY_OP",
        }

        self.available_bin_operators = {
            0: "+",
            1: "&",
            2: "//",
            3: "<<",
            5: "*",
            6: "%",
            7: "|",
            8: "**",
            9: ">>",
            10: "-",
            11: "/",
            12: "^",
            13: "+=",
            14: "&=",
            15: "//=",
            16: "<<=",
            18: "*=",
            19: "%=",
            20: "|=",
            21: "**=",
            22: ">>=",
            23: "-=",
            24: "/=",
            25: "^=",
        }

        self.available_cmp_operators = {
            2: "<",
            26: "<=",
            40: "==",
            55: "!=",
            68: ">",
            92: ">=",
        }

        self.available_identity_operators = {
            0: "is",
            1: "is not",
        }

        self.available_contains_operators = {
            0: "in",
            1: "not in",
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

        self.stack.PUSH(eval(f"{lhs} {self.available_bin_operators[operator]} {rhs}"))

    def COMPARE_OP(self, operator):
        if self.stack.top < 1:
            print("STACK UNDERFLOW -- NOT ENOUGH ELEMENTS")
            return

        if operator not in self.available_cmp_operators:
            print("INVALID OPERATOR")
            return

        rhs = self.stack.POP_TOP()
        lhs = self.stack.POP_TOP()

        self.stack.PUSH(eval(f"{lhs} {self.available_cmp_operators[operator]} {rhs}"))

    def IS_OP(self, operator):
        if self.stack.top < 1:
            print("STACK UNDERFLOW -- NOT ENOUGH ELEMENTS")
            return

        if operator not in self.available_identity_operators:
            print("INVALID OPERATOR")
            return

        rhs = self.stack.POP_TOP()
        lhs = self.stack.POP_TOP()

        self.stack.PUSH(eval(f"{lhs} {self.available_identity_operators[operator]} {rhs}"))

    def CONTAINS_OP(self, operator):
        if self.stack.top < 1:
            print("STACK UNDERFLOW -- NOT ENOUGH ELEMENTS")
            return

        if operator not in self.available_contains_operators:
            print("INVALID OPERATOR")
            return

        rhs = self.stack.POP_TOP()
        lhs = self.stack.POP_TOP()

        self.stack.PUSH(eval(f"{lhs} {self.available_contains_operators[operator]} {rhs}"))