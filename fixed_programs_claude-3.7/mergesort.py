# Fixed Program: mergesort (Claude 3.7 Sonnet)
# Bug Classification: Incorrect comparison operator
# Bug Description: The merge function incorrectly used the logical 'or' operator (left[i:] or right[j:]) which only evaluates to the first truthy value. This means if left[i:] is non-empty, right[j:] will be ignored completely. This leads to missing elements in the final sorted result when both arrays have remaining elements.
# Fixed on: 2025-05-27 22:52:05
# LLM Used: Claude 3.7 Sonnet
# 
# Original bug was classified as: Incorrect comparison operator
# This indicates: The merge function incorrectly used the logical 'or' operator (left[i:] or right[j:]) which only evaluates to the first truthy value. This means if left[i:] is non-empty, right[j:] will be ignored completely. This leads to missing elements in the final sorted result when both arrays have remaining elements.

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
        result.extend(left[i:])
        result.extend(right[j:])
        return result

    if len(arr) == 0:
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