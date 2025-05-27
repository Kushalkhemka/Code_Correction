# Fixed Program: mergesort (DeepSeek)
# Bug Classification: Missing condition
# Bug Description: The 'or' operator in 'left[i:] or right[j:]' does not correctly handle the case where one of the slices is empty. The intended logic is to append all remaining elements from both sublists.
# Fixed on: 2025-05-27 12:52:54
# LLM Used: DeepSeek
# 
# Original bug was classified as: Missing condition
# This indicates: The 'or' operator in 'left[i:] or right[j:]' does not correctly handle the case where one of the slices is empty. The intended logic is to append all remaining elements from both sublists.


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