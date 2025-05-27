# Fixed Program: mergesort (Claude 3.5 Sonnet)
# Bug Classification: Missing condition
# Bug Description: The base case condition in mergesort was incomplete - it only checked for empty arrays (len(arr) == 0) but didn't handle single-element arrays as a base case. Single-element arrays are already sorted by definition and should be returned immediately.
# Fixed on: 2025-05-27 13:42:01
# LLM Used: Claude 3.5 Sonnet
# 
# Original bug was classified as: Missing condition
# This indicates: The base case condition in mergesort was incomplete - it only checked for empty arrays (len(arr) == 0) but didn't handle single-element arrays as a base case. Single-element arrays are already sorted by definition and should be returned immediately.

def mergesort(arr):
    def merge(left, right):
        result = []
        i = 0
        j = 0
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        result.extend(left[i:] or right[j:])
        return result

    if len(arr) <= 1:
        return arr
    else:
        middle = len(arr) // 2
        left = mergesort(arr[:middle])
        right = mergesort(arr[middle:])
        return merge(left, right)


"""
Merge Sort


Input:
    arr: A list of ints

Output:
    The elements of arr in sorted order
"""