# Fixed Program: rpn_eval (Claude 3.7 Sonnet)
# Bug Classification: Variable swap
# Bug Description: The operands 'a' and 'b' were passed in the wrong order to the op function. In Reverse Polish Notation, when evaluating operations, the first value popped (a) is the second operand, and the second value popped (b) is the first operand. This causes incorrect results for non-commutative operations like subtraction and division.
# Fixed on: 2025-05-27 22:58:07
# LLM Used: Claude 3.7 Sonnet
# 
# Original bug was classified as: Variable swap
# This indicates: The operands 'a' and 'b' were passed in the wrong order to the op function. In Reverse Polish Notation, when evaluating operations, the first value popped (a) is the second operand, and the second value popped (b) is the first operand. This causes incorrect results for non-commutative operations like subtraction and division.

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
            a = stack.pop()
            b = stack.pop()
            stack.append(
                op(token, b, a)
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