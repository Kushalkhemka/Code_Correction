# Fixed Program: rpn_eval (DeepSeek)
# Bug Classification: Variable swap
# Bug Description: The bug occurs because the operands are popped in the wrong order for operations like subtraction and division. The first popped value should be the second operand, and the second popped value should be the first operand. Currently, the order is reversed, leading to incorrect results.
# Fixed on: 2025-05-27 12:52:46
# LLM Used: DeepSeek
# 
# Original bug was classified as: Variable swap
# This indicates: The bug occurs because the operands are popped in the wrong order for operations like subtraction and division. The first popped value should be the second operand, and the second popped value should be the first operand. Currently, the order is reversed, leading to incorrect results.

def rpn_eval(tokens):
    def op(symbol, a, b):
        return {
            '+': lambda a, b: a + b,
            '-': lambda a, b: a - b,
            '*': lambda a, b: a * b,
            '/': lambda a, b: a / b
        }[symbol](a, b)

    stack = []
 
    for token in tokens:
        if isinstance(token, float):
            stack.append(token)
        else:
            b = stack.pop()
            a = stack.pop()
            stack.append(
                op(token, a, b)
            )

    return stack.pop()


"""
Reverse Polish Notation

Four-function calculator with input given in Reverse Polish Notation (RPN).

Input:
    A list of values and operators encoded as floats and strings

Precondition:
    all(
        isinstance(token, float) or token in ('+', '-', '*', '/') for token in tokens
    )

Example:
    >>> rpn_eval([3.0, 5.0, '+', 2.0, '/'])
    4.0
"""