# Fixed Program: next_permutation (Claude 3.7 Sonnet)
# Bug Classification: Incorrect comparison operator
# Bug Description: The algorithm was using an incorrect comparison operator when finding the rightmost element to swap with. It was looking for elements smaller than perm[i] when it should be looking for elements larger than perm[i].
# Fixed on: 2025-05-27 22:53:43
# LLM Used: Claude 3.7 Sonnet
# 
# Original bug was classified as: Incorrect comparison operator
# This indicates: The algorithm was using an incorrect comparison operator when finding the rightmost element to swap with. It was looking for elements smaller than perm[i] when it should be looking for elements larger than perm[i].

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