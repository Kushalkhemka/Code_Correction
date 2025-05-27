# Fixed Program: find_first_in_sorted (Claude 3.7 Sonnet)
# Bug Classification: Incorrect comparison operator
# Bug Description: The binary search was using 'x <= arr[mid]' as a condition to search the left half of the array, which could cause the algorithm to miss the first occurrence of a value that appears multiple times. When x equals arr[mid], we should continue searching in the right half unless we've confirmed it's the first occurrence.
# Fixed on: 2025-05-27 22:44:20
# LLM Used: Claude 3.7 Sonnet
# 
# Original bug was classified as: Incorrect comparison operator
# This indicates: The binary search was using 'x <= arr[mid]' as a condition to search the left half of the array, which could cause the algorithm to miss the first occurrence of a value that appears multiple times. When x equals arr[mid], we should continue searching in the right half unless we've confirmed it's the first occurrence.

def find_first_in_sorted(arr, x):
    lo = 0
    hi = len(arr)

    while lo <= hi:
        mid = (lo + hi) // 2

        if x == arr[mid] and (mid == 0 or x != arr[mid - 1]):
            return mid

        elif x < arr[mid]:
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