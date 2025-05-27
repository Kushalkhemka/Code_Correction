# Fixed Program: lis (Claude 3.7 Sonnet)
# Bug Classification: Missing condition
# Bug Description: The condition on line 8 was missing a check to ensure 'length + 1' is a valid key in the 'ends' dictionary before accessing it. When length equals longest, the code would try to access 'ends[length + 1]', which doesn't exist yet, causing a KeyError. The second part of the condition should only be evaluated when length < longest.
# Fixed on: 2025-05-27 22:50:28
# LLM Used: Claude 3.7 Sonnet
# 
# Original bug was classified as: Missing condition
# This indicates: The condition on line 8 was missing a check to ensure 'length + 1' is a valid key in the 'ends' dictionary before accessing it. When length equals longest, the code would try to access 'ends[length + 1]', which doesn't exist yet, causing a KeyError. The second part of the condition should only be evaluated when length < longest.

def lis(arr):
    ends = {}
    longest = 0

    for i, val in enumerate(arr):

        prefix_lengths = [j for j in range(1, longest + 1) if arr[ends[j]] < val]

        length = max(prefix_lengths) if prefix_lengths else 0

        if length == longest or (length < longest and val < arr[ends[length + 1]]):
            ends[length + 1] = i
            longest = max(longest, length + 1)

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