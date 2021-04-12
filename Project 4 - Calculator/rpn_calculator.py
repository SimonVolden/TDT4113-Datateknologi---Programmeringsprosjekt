"""RPN CALCULATOR"""
import numbers
import re
import numpy
from container import Stack, Queue


class Function:
    """class for functions"""

    def __init__(self, func):
        self.func = func

    def execute(self, element, debug=True):
        """Execute function"""
        # Check type
        if not isinstance(element, numbers.Number):
            raise TypeError("The element must be a number")
        result = self.func(element)

        # Report
        if debug is True:
            print("Function: " + self.func.__name__
                  + "({:f}) = {:f}".format(element, result))

        return result


class Operator:
    """Class for operations"""

    def __init__(self, operation, strength):
        self.operation = operation
        self.strength = strength

    def execute(self, i, j, debug=True):
        if not isinstance(i, numbers.Number) or not isinstance(j, numbers.Number):
            raise TypeError("Elements must be numbers")
        result = self.operation(i, j)
        if debug:
            print("Operation: " + self.operation.__name__
                  + "({:f}, {:f}) = {:f}".format(i, j, result))
        return result


class Calculator:
    def __init__(self):
        self.functions = {"EXP": Function(numpy.exp),
                          "LOG": Function(numpy.log),
                          "SIN": Function(numpy.sin),
                          "COS": Function(numpy.cos),
                          "SQRT": Function(numpy.sqrt)}

        self.operators = {"ADD": Operator(numpy.add, 0),
                          "PLUS": Operator(numpy.add, 0),
                          "MULTIPLY": Operator(numpy.multiply, 1),
                          "TIMES": Operator(numpy.multiply, 1),
                          "DIVIDE": Operator(numpy.divide, 2),
                          "SUBTRACT": Operator(numpy.subtract, 0),
                          "MINUS": Operator(numpy.subtract, 0)}

        self.input_queue = Queue()
        self.output_queue = Queue()
        self.operator_stack = Stack()

    def fill_output_queue(self, input_list):
        for i in input_list:
            self.output_queue.push(i)

    def fill_input_queue(self, input_list):
        for i in input_list:
            self.input_queue.push(i)

    def rpn_with_strings(self):
        stack = Stack()

        while not self.output_queue.is_empty():
            i = self.output_queue.pop()

            if isinstance(i, numbers.Number):
                stack.push(i)

            elif (i == "EXP") or (i == "LOG") or (i == "SIN") or (i == "COS") or (i == "SQRT"):
                number = stack.pop()
                self.output_queue.push(self.functions[i].execute(number))

            elif ((i == "ADD") or (i == "PLUS") or (i == "MULTIPLY") or (i == "TIMES") or (i == "DIVIDE")
                  or (i == "SUBTRACT") or (i == "MINUS")):
                number2 = stack.pop()
                number1 = stack.pop()
                stack.push(self.operators[i].execute(number1, number2))

        return stack.pop()

    def rpn(self):
        stack = Stack()

        while not self.output_queue.is_empty():
            i = self.output_queue.pop()

            if isinstance(i, numbers.Number):
                stack.push(i)

            elif isinstance(i, Function):
                number = stack.pop()
                self.output_queue.push(i.execute(number))

            elif isinstance(i, Operator):
                number2 = stack.pop()
                number1 = stack.pop()
                stack.push(i.execute(number1, number2))

        return stack.pop()

    def normal_notation(self):

        while not self.input_queue.is_empty():

            if isinstance(self.input_queue.peek(), numbers.Number):
                self.output_queue.push(self.input_queue.pop(),)

            elif isinstance(self.input_queue.peek(), Function):
                self.operator_stack.push(self.input_queue.pop())

            elif self.input_queue.peek() == "(":
                self.operator_stack.push(self.input_queue.pop())

            elif self.input_queue.peek() == ")":
                while self.operator_stack.peek() != "(":
                    self.output_queue.push(self.operator_stack.pop())
                if self.operator_stack.peek() == "(":
                    self.operator_stack.pop()
                if isinstance(self.operator_stack.peek(), Function):
                    self.output_queue.push(self.operator_stack.pop())
                self.input_queue.pop()

            elif isinstance(self.input_queue.peek(), Operator):
                while not self.operator_stack.is_empty():
                    if isinstance(self.operator_stack.peek(), Operator):
                        if self.operator_stack.peek().strength < self.input_queue.peek().strength:
                            break
                    if self.operator_stack.peek() == "(":
                        break
                    self.output_queue.push(self.operator_stack.pop())
                self.operator_stack.push(self.input_queue.pop())

        while not self.operator_stack.is_empty():
            self.output_queue.push(self.operator_stack.pop())

        return self.rpn()

    def parse(self, input_string):

        input_queue = []
        text = input_string.replace(" ", "").upper()

        function_targets = "|".join(["^" + func for func in self.functions.keys()])
        operators_targets = "|".join(["^" + op for op in self.operators.keys()])
        string_targets = r'^\(|^\)'
        float_targets = "^[-0123456789.]+"

        while len(text) > 0:
            if re.search(string_targets, text) is not None:
                match = re.search(string_targets, text)
                input_queue.append(match.group(0))
                text = text[match.end(0):]

            elif re.search(function_targets, text) is not None:
                match = re.search(function_targets, text)
                input_queue.append(self.functions[match.group(0)])
                text = text[match.end(0):]

            elif re.search(operators_targets, text) is not None:
                match = re.search(operators_targets, text)
                input_queue.append(self.operators[match.group(0)])
                text = text[match.end(0):]

            elif re.search(float_targets, text) is not None:
                match = re.search(float_targets, text)
                input_queue.append(float(match.group(0)))
                text = text[match.end(0):]

            else:
                print("invalid input")
                return

        return input_queue

    def calculate_expression(self, text):
        self.fill_input_queue(self.parse(text))
        return self.normal_notation()

#Testing

if __name__ == "__main__":
    print("TESTING")
    calc = Calculator()
    assert calc.calculate_expression("2 multiply 4") == 8, "Should be 8"
    assert calc.calculate_expression("((15 divide (7 subtract (1 add 1))) multiply 3) subtract (2 add (1 add 1))"), "Should be 5"
    assert calc.calculate_expression("exp(1 add 2 multiply 3)"), "Should be 1096.633158"
    calc.calculate_expression("8 subtract -2")
