# Fixed Program: shunting_yard (Claude 3.5 Sonnet)
# Bug Classification: Missing line
# Bug Description: The code was missing the crucial line to append the current operator token to the operator stack after processing higher precedence operators, causing operators to be lost during processing.
# Fixed on: 2025-05-27 13:41:55
# LLM Used: Claude 3.5 Sonnet
# 
# Original bug was classified as: Missing line
# This indicates: The code was missing the crucial line to append the current operator token to the operator stack after processing higher precedence operators, causing operators to be lost during processing.

def shunting_yard(tokens):
    precedence = {
        '+': 1,
        '-': 1,
        '*': 2,
        '/': 2
    }

    rpntokens = []
    opstack = []
    for token in tokens:
        if isinstance(token, int):
            rpntokens.append(token)
        else:
            while opstack and precedence[token] <= precedence[opstack[-1]]:
                rpntokens.append(opstack.pop())
            opstack.append(token)  # Added missing line to push current operator to stack
 
    while opstack:
        rpntokens.append(opstack.pop())

    return rpntokens


"""
Infix to RPN Conversion
shunting-yard


Uses Dijkstra's shunting-yard algorithm to transform infix notation into equivalent Reverse Polish Notation.

Input:
    tokens: A list of tokens in infix notation

Precondition:
    all(isinstance(token, int) or token in '+-*/' for token in tokens)

Output:
    The input tokens reordered into Reverse Polish Notation

Examples:
    >>> shunting_yard([10, '-', 5, '-', 2])
    [10, 5, '-', 2, '-']
    >>> shunting_yard([34, '-', 12, '/', 5])
    [34, 12, 5, '/' ,'-']
    >>> shunting_yard([4, '+', 9, '*', 9, '-', 10, '+', 13])
    [4, 9, 9, '*', '+', 10, '-', 13, '+']
"""