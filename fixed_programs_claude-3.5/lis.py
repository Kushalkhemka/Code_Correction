# Fixed Program: lis (Claude 3.5 Sonnet)
# Bug Classification: Missing/added +1
# Bug Description: Missing +1 when calculating the length of a new subsequence that extends a previous prefix. The code assigns just the maximum prefix length instead of adding 1 to account for the new element being added.
# Fixed on: 2025-05-27 13:42:00
# LLM Used: Claude 3.5 Sonnet
# 
# Original bug was classified as: Missing/added +1
# This indicates: Missing +1 when calculating the length of a new subsequence that extends a previous prefix. The code assigns just the maximum prefix length instead of adding 1 to account for the new element being added.

def lis(arr):
    ends = {}
    longest = 0

    for i, val in enumerate(arr):

        prefix_lengths = [j for j in range(1, longest + 1) if arr[ends[j]] < val]

        length = max(prefix_lengths) + 1 if prefix_lengths else 0

        if length == longest or val < arr[ends[length + 1]]:
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