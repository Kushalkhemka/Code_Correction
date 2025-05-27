# Fixed Program: sieve (Claude 3.5 Sonnet)
# Bug Classification: Incorrect comparison operator
# Bug Description: The comparison operator '> 0' was incorrectly used to check for primality, causing the algorithm to identify composite numbers instead of primes. The condition needed to be '== 0' with a negation of the entire expression.
# Fixed on: 2025-05-27 13:42:00
# LLM Used: Claude 3.5 Sonnet
# 
# Original bug was classified as: Incorrect comparison operator
# This indicates: The comparison operator '> 0' was incorrectly used to check for primality, causing the algorithm to identify composite numbers instead of primes. The condition needed to be '== 0' with a negation of the entire expression.

def sieve(max):
    primes = []
    for n in range(2, max + 1):
        if not any(n % p == 0 for p in primes):
            primes.append(n)
    return primes

"""
Sieve of Eratosthenes
prime-sieve

Input:
    max: A positive int representing an upper bound.

Output:
    A list containing all primes up to and including max
"""