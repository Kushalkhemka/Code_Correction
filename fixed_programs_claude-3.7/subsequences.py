# Fixed Program: subsequences (Claude 3.7 Sonnet)
# Bug Classification: Incorrect array slice
# Bug Description: The range in the for loop was incorrectly set to 'range(a, b + 1 - k)', which limits the starting positions for subsequences. This prevented the function from considering all valid starting positions, especially those close to the upper bound b, resulting in missing valid subsequences.
# Fixed on: 2025-05-27 23:02:15
# LLM Used: Claude 3.7 Sonnet
# 
# Original bug was classified as: Incorrect array slice
# This indicates: The range in the for loop was incorrectly set to 'range(a, b + 1 - k)', which limits the starting positions for subsequences. This prevented the function from considering all valid starting positions, especially those close to the upper bound b, resulting in missing valid subsequences.

def subsequences(a, b, k):
    if k == 0:
        return []

    ret = []
    for i in range(a, b - k + 2):
        ret.extend(
            [i] + rest for rest in subsequences(i + 1, b, k - 1)
        )

    return ret


"""
Subsequences

 
Input:
    a: An int
    b: An int
    k: A positive int

Output:
    A list of all length-k ascending sequences of ints in range(a, b)

Example:
    >>> subsequences(a=1, b=5, k=3)
    [[1, 2, 3], [1, 2, 4], [1, 3, 4], [2, 3, 4]]
"""