# Fixed Program: find_first_in_sorted (DeepSeek)
# Bug Classification: Incorrect comparison operator
# Bug Description: The loop condition 'lo <= hi' was incorrect, leading to potential infinite loops or incorrect results. The condition was changed to 'lo < hi' to ensure proper termination. Additionally, the initial value of 'hi' was corrected to 'len(arr) - 1' to avoid out-of-bounds errors, and the comparison 'x <= arr[mid]' was changed to 'x < arr[mid]' for accurate search behavior.
# Fixed on: 2025-05-27 12:52:58
# LLM Used: DeepSeek
# 
# Original bug was classified as: Incorrect comparison operator
# This indicates: The loop condition 'lo <= hi' was incorrect, leading to potential infinite loops or incorrect results. The condition was changed to 'lo < hi' to ensure proper termination. Additionally, the initial value of 'hi' was corrected to 'len(arr) - 1' to avoid out-of-bounds errors, and the comparison 'x <= arr[mid]' was changed to 'x < arr[mid]' for accurate search behavior.

def find_first_in_sorted(arr, x):
    lo = 0
    hi = len(arr) - 1

    while lo < hi:
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