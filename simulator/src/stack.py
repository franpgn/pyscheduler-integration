class Stack:
    def __init__(self, size):
        self.stack = []
        self.size = size
        self.top = -1
        self.empty = True
        self.available_instructions = {
            1: "POP_TOP",
            4: "END_FOR",
            5: "END_SEND",
            9: "NOP",
            83: "RETURN_VALUE",
            99: "SWAP",
            120: "COPY",
        }

    def SHOW_STACK(self):
        if self.empty:
            print("EMPTY STACK")
            print()
            return

        print("STACK:")
        for i in range(self.top, -1, -1):
            print(self.stack[i] if i != self.top else f"{self.stack[i]} <-- TOS")
        print("EOS")
        print()

    def NOP(self):
        pass

    def RETURN_VALUE(self):
        if self.empty:
            return None
        return self.stack[self.top]

    def PUSH(self, value):
        if self.top == self.size - 1:
            print("STACK OVERFLOW")
            return

        self.stack.append(value)
        self.top += 1
        self.empty = False

    def POP_TOP(self):
        if self.empty:
            print("STACK UNDERFLOW -- EMPTY STACK")
            return

        self.top -= 1
        if self.top == -1:
            self.empty = True

        return self.stack.pop()

    def END_FOR(self):
        for i in range(2):
            if self.empty:
                print("STACK UNDERFLOW -- EMPTY STACK" if i == 0 else "STACK UNDERFLOW -- ONE ELEMENT REMOVED")
                return

            self.stack.pop()
            self.top -= 1
            if self.top == -1:
                self.empty = True

    def END_SEND(self):
        if self.top < 1:
            print("STACK UNDERFLOW -- NOT ENOUGH ELEMENTS")
            return

        del self.stack[-2]
        self.top -= 1

    def COPY(self, index):
        if index < 0:
            print("INDEX MUST BE GREATER THAN -1")
            return

        if self.top < index:
            print("STACK UNDERFLOW -- INDEX OUT OF RANGE")
            return

        self.PUSH(self.stack[-index])

    def SWAP(self, index):
        if index < 0:
            print("INDEX MUST BE GREATER THAN -1")
            return

        if self.top < index:
            print("STACK UNDERFLOW -- INDEX OUT OF RANGE")
            return

        self.stack[self.top], self.stack[-index] = self.stack[-index], self.stack[self.top]

    def FETCH_POS(self, index):
        if index < 0 or index > self.top:
            print("INDEX OUT OF RANGE")
            return

        return self.stack[-index]