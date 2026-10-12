from typing import Callable, Dict
from sys import argv

class StackMachin:
    __stack: list[int] = []
    __operation: dict[str, Callable[[],int]]
    __items: list[str] = []

    def __init__(self) -> None:
        self.__operation = {"+": self.__plus,
                            "-": self.__minus,
                            "*": self.__mul,
                            "/": self.__div,
                            "~": self.__tilda}

    def start(self, input_line: str)->int:
        self.__items = self.is_empty(input_line).split(" ")
        for s in self.__items:
            if s not in "/*+-~":
                self.__stack.append(int(s))
                print(self.__stack)
            elif s in "/*+-~":
                num = self.__operation[s]()
                self.__stack.append(num)
            else:
                raise ValueError("wrong letter","line must have nums, spaces or any element like -*/+~")
        return self.__stack.pop()
    
    def __plus(self) -> int:
        print("plus:",self.__stack)
        total = 0
        while self.__stack :
            total += self.__stack.pop()
        return total
    
    def __minus(self) -> int:
        print("minus:",self.__stack)
        total = 0
        while self.__stack :
            total -= self.__stack.pop()
        return total
        

    def __mul(self) -> int:
        total = 1
        print("multply:",self.__stack)

        while self.__stack:
            total *= self.__stack.pop()
        return total

    def __div(self) -> int:
        print("div:",self.__stack)
        delimeter = self.__stack.pop()
        return self.__operation["+"]() / delimeter

    def __tilda(self) -> int:
        print("tilda:",self.__stack)
        num1 = self.__stack.pop()
        num2 = self.__stack.pop()
        if num1 and num2:
            return abs(num1-num2)
        return self.__operation["+"]() ** 2

    def is_empty(self, line: str) -> str:
        if len(line) == 0:
            raise NameError("empty line", "line must be not empty")
        return line
    


if __name__ == "__main__":
    if len(argv) == 2:
        if argv[1] != "-h":
            try:
                stack = StackMachin()
                print(stack.start(argv[1]))
            except Exception as e:
                print(f"Something happend\nError: {e}")
                print("In next time you should be more carefully")
        else:
            print(
"""Hello, I'm a stack machine.
I support operation +*/-~.
What is a operator ~ ? 
If both operands are not 0: compute the absolute value of the difference `|x - y|` and push the result back onto the stack.
If at least one of the operands is 0: calculates the sum of all values on the stack, squares it, and pushes the result back onto the stack.
""")
        
    else:
        print('Wrong arguments. You should call a flag "-h" to find out more information about app.')