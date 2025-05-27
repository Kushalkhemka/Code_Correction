# Fixed Program: bitcount (Claude 3.7 Sonnet)
# Bug Classification: Incorrect assignment operator
# Bug Description: The code incorrectly used the XOR assignment operator (^=) instead of the AND assignment operator (&=) in Brian Kernighan's bit counting algorithm. The correct algorithm requires using 'n &= (n-1)' to clear the least significant set bit in each iteration, allowing an accurate count of the number of set bits.
# Fixed on: 2025-05-27 22:41:36
# LLM Used: Claude 3.7 Sonnet
# 
# Original bug was classified as: Incorrect assignment operator
# This indicates: The code incorrectly used the XOR assignment operator (^=) instead of the AND assignment operator (&=) in Brian Kernighan's bit counting algorithm. The correct algorithm requires using 'n &= (n-1)' to clear the least significant set bit in each iteration, allowing an accurate count of the number of set bits.

def bitcount(n):
    count = 0
    while n:
        n &= n - 1
        count += 1
    return count

 
"""
Bitcount
bitcount


Input:
    n: a nonnegative int

Output:
    The number of 1-bits in the binary encoding of n

Examples:
    >>> bitcount(127)
    7
    >>> bitcount(128)
    1
"""