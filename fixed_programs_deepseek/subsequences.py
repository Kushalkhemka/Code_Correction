# Fixed Program: subsequences (DeepSeek)
# Bug Classification: Missing/added +1
# Bug Description: The upper bound of the range excluded the last valid starting point for a subsequence of length k. The fix ensures the range includes all valid starting points by adjusting the upper bound to 'b - k + 2'.
# Fixed on: 2025-05-27 12:52:49
# LLM Used: DeepSeek
# 
# Original bug was classified as: Missing/added +1
# This indicates: The upper bound of the range excluded the last valid starting point for a subsequence of length k. The fix ensures the range includes all valid starting points by adjusting the upper bound to 'b - k + 2'.

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