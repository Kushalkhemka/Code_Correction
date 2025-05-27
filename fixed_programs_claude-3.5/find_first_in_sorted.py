# Fixed Program: find_first_in_sorted (Claude 3.5 Sonnet)
# Bug Classification: Incorrect comparison operator
# Bug Description: The code used '!=' instead of '>' when checking for the first occurrence of x in a sorted array. This could lead to incorrect results when there are values different from but greater than x before the first occurrence of x.
# Fixed on: 2025-05-27 13:42:05
# LLM Used: Claude 3.5 Sonnet
# 
# Original bug was classified as: Incorrect comparison operator
# This indicates: The code used '!=' instead of '>' when checking for the first occurrence of x in a sorted array. This could lead to incorrect results when there are values different from but greater than x before the first occurrence of x.

def find_first_in_sorted(arr, x):
    lo = 0
    hi = len(arr)

    while lo <= hi:
        mid = (lo + hi) // 2

        if x == arr[mid] and (mid == 0 or x > arr[mid - 1]):
            return mid

        elif x <= arr[mid]:
            hi = mid

        else:
            lo = mid + 1

    return -1

 
"""
Fancy Binary Search
fancy-binsearch


Input:
    arr: A sorted list of ints
    x: A value to find

Output:
    The lowest index i such that arr[i] == x, or -1 if x not in arr

Example:
    >>> find_first_in_sorted([3, 4, 5, 5, 5, 5, 6], 5)
    2
"""