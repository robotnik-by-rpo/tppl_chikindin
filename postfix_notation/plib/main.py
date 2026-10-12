from typing import Callable, Dict
from sys import argv

class StackMachin:


    def __init__(self) -> None:
        self.__operation = {"+": self.__plus,
                            "-": self.__minus,
                            "*": self.__mul,
                            "/": self.__div,
                            "~": self.__tilda}
        self.__stack: list[int] = []
        self.__operation: dict[str, Callable[[],int]]
        self.__items: list[str] = []

    def start(self, input_line: str)->int:
        self.__items = self.is_empty(input_line).split()
        for s in self.__items:
            if s in self.__operation:
                num = self.__operation[s]()
                print(self.__stack, "<-", num)
                self.__stack.append(num)
            else:
                print(self.__stack, "<-", s)
                self.__stack.append(int(s))
        return self.__stack.pop()
    
    def __plus(self) -> int:
        b = self.__stack.pop()
        a = self.__stack.pop()
        print("plus:",self.__stack,"->",a,b)
        return a + b

    
    def __minus(self) -> int:
        print("minus:",self.__stack)
        b = self.__stack.pop()
        a = self.__stack.pop()
        print("minus:",self.__stack,"->",a,b)
        return a - b
        

    def __mul(self) -> int:
        b = self.__stack.pop()
        a = self.__stack.pop()
        print("multiply:",self.__stack,"->",a,b)
        return a * b

    def __div(self) -> int:
        print("div:", self.__stack)
        divisor = self.__stack.pop()
        dividend = self.__stack.pop()
        if divisor == 0:
            raise ZeroDivisionError("division by zero", "delimeter must be not zero value")
        print("plus:",self.__stack,"->",divisor,dividend)
        return dividend // divisor

    def __tilda(self) -> int:
        
        b = self.__stack.pop()
        a = self.__stack.pop()
        print("tilda:",self.__stack,"->",a,b)
        if a and b:
            return abs(a - b)
        total = 0
        while self.__stack:
            total += self.__stack.pop()
        return total ** 2

    def is_empty(self, line: str) -> str:
        if len(line.strip()) == 0:
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
Example call in path ./postfix_notation/plib:
python3 main.py "5 3 +"
Example call from Makefile in root directory:
make run EXP="5 3 +"
""")
        
    else:
        print('Wrong arguments. You should call a flag "-h" to find out more information about app.')