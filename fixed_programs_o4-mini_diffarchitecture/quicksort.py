def quicksort(arr):
    if not isinstance(arr, list):
        raise TypeError("Input must be a list.")
    if len(arr) <= 1:
        return arr
    if len(arr) > 2:
        mid = len(arr) // 2
        candidates = [(arr[0], 0), (arr[mid], mid), (arr[-1], len(arr) - 1)]
        pivot, pivot_index = sorted(candidates, key=lambda x: x[0])[1]
    else:
        pivot, pivot_index = arr[0], 0
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
    return quicksort(less_than_pivot) + [pivot] * pivot_count + quicksort(greater_than_pivot)