# Fixed Program: next_permutation (DeepSeek)
# Bug Classification: Incorrect comparison operator
# Bug Description: The condition `if perm[j] < perm[i]` was incorrect; it should be `if perm[j] > perm[i]` to find the smallest element greater than `perm[i]` for generating the next lexicographical permutation.
# Fixed on: 2025-05-27 12:52:45
# LLM Used: DeepSeek
# 
# Original bug was classified as: Incorrect comparison operator
# This indicates: The condition `if perm[j] < perm[i]` was incorrect; it should be `if perm[j] > perm[i]` to find the smallest element greater than `perm[i]` for generating the next lexicographical permutation.

def next_permutation(perm):
    for i in range(len(perm) - 2, -1, -1):
        if perm[i] < perm[i + 1]:
            for j in range(len(perm) - 1, i, -1):
                if perm[j] > perm[i]:
                    next_perm = list(perm)
                    next_perm[i], next_perm[j] = perm[j], perm[i]
                    next_perm[i + 1:] = reversed(next_perm[i + 1:])
                    return next_perm


"""
Next Permutation
next-perm


Input:
    perm: A list of unique ints

Precondition:
    perm is not sorted in reverse order

Output:
    The lexicographically next permutation of the elements of perm

Example:
    >>> next_permutation([3, 2, 4, 1])
    [3, 4, 1, 2]
"""