def quicksort(arr):
    """
    Sorts an array using the quicksort algorithm.
    
    This function implements the quicksort algorithm to sort a list of elements. It includes improvements
    for handling duplicates, efficient partitioning, and better pivot selection to optimize performance.
    
    Parameters:
    arr (list): The list of elements to be sorted.
    
    Returns:
    list: A new list that is the sorted version of the input list.
    
    Raises:
    TypeError: If the input is not a list.
    """
    if not isinstance(arr, list):
        raise TypeError("Input must be a list.")
    
    if len(arr) <= 1:
        return arr
    
    # Improved pivot selection: median-of-three
    if len(arr) > 2:
        mid = len(arr) // 2
        candidates = [(arr[0], 0), (arr[mid], mid), (arr[-1], -1)]
        # Sort candidates based on values and choose the median
        pivot, pivot_index = sorted(candidates, key=lambda x: x[0])[1]
    else:
        pivot, pivot_index = arr[0], 0
    
    # Single pass partitioning
    less_than_pivot = []
    greater_than_pivot = []
    pivot_count = 0
    
    for x in arr:
        if x < pivot:
            less_than_pivot.append(x)
        elif x > pivot:
            greater_than_pivot.append(x)
        else:
            pivot_count += 1
    
    # Recursively apply quicksort and combine results
    return quicksort(less_than_pivot) + [pivot] * pivot_count + quicksort(greater_than_pivot)

# Example usage:
sorted_array = quicksort([3, 6, 8, 10, 1, 2, 1])
print("Sorted array:", sorted_array)