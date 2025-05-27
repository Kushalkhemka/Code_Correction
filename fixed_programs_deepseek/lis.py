# Fixed Program: lis (DeepSeek)
# Bug Classification: Missing condition
# Bug Description: The code assumes `ends[length + 1]` exists, but this is not always true, leading to a `KeyError`. A condition is missing to handle cases where `length + 1` exceeds `longest`.
# Fixed on: 2025-05-27 12:52:53
# LLM Used: DeepSeek
# 
# Original bug was classified as: Missing condition
# This indicates: The code assumes `ends[length + 1]` exists, but this is not always true, leading to a `KeyError`. A condition is missing to handle cases where `length + 1` exceeds `longest`.

def lis(arr):
    ends = {}
    longest = 0

    for i, val in enumerate(arr):

        prefix_lengths = [j for j in range(1, longest + 1) if arr[ends[j]] < val]

        length = max(prefix_lengths) if prefix_lengths else 0

        if length == longest or (length + 1 <= longest and val < arr[ends[length + 1]]):
            ends[length + 1] = i
            longest = length + 1

    return longest


"""
Longest Increasing Subsequence
longest-increasing-subsequence


Input:
    arr: A sequence of ints

Precondition:
    The ints in arr are unique

Output:
    The length of the longest monotonically increasing subsequence of arr

Example:
    >>> lis([4, 1, 5, 3, 7, 6, 2])
    3
"""