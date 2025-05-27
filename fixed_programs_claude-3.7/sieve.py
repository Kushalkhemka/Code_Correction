# Fixed Program: sieve (Claude 3.7 Sonnet)
# Bug Classification: Incorrect comparison operator
# Bug Description: The condition used any(n % p > 0) which checks if n is NOT divisible by AT LEAST ONE prime, when it should be checking if n is not divisible by ANY previous prime. This caused composite numbers to be incorrectly included in the list of primes.
# Fixed on: 2025-05-27 23:01:09
# LLM Used: Claude 3.7 Sonnet
# 
# Original bug was classified as: Incorrect comparison operator
# This indicates: The condition used any(n % p > 0) which checks if n is NOT divisible by AT LEAST ONE prime, when it should be checking if n is not divisible by ANY previous prime. This caused composite numbers to be incorrectly included in the list of primes.

def sieve(max):
    primes = []
    for n in range(2, max + 1):
        if all(n % p != 0 for p in primes):
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