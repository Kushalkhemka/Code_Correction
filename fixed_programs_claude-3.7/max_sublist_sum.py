# Fixed Program: max_sublist_sum (Claude 3.7 Sonnet)
# Bug Classification: Incorrect variable
# Bug Description: The algorithm initializes max_so_far to 0, which is incorrect when all elements in the array are negative. In that case, the function would return 0 instead of the largest negative value. For example, max_sublist_sum([-4, -4, -5]) would incorrectly return 0, but the maximum sublist sum should be -4.
# Fixed on: 2025-05-27 22:51:32
# LLM Used: Claude 3.7 Sonnet
# 
# Original bug was classified as: Incorrect variable
# This indicates: The algorithm initializes max_so_far to 0, which is incorrect when all elements in the array are negative. In that case, the function would return 0 instead of the largest negative value. For example, max_sublist_sum([-4, -4, -5]) would incorrectly return 0, but the maximum sublist sum should be -4.

def max_sublist_sum(arr):
    if not arr:
        return 0
        
    max_ending_here = arr[0]
    max_so_far = arr[0]

    for x in arr[1:]:
        max_ending_here = max(x, max_ending_here + x)
        max_so_far = max(max_so_far, max_ending_here)

    return max_so_far

 
"""
Max Sublist Sum
max-sublist-sum

Efficient equivalent to max(sum(arr[i:j]) for 0 <= i <= j <= len(arr))

Algorithm source: WordAligned.org by Thomas Guest


Input:
    arr: A list of ints

Output:
    The maximum sublist sum

Example:
    >>> max_sublist_sum([4, -5, 2, 1, -1, 3])
    5
"""