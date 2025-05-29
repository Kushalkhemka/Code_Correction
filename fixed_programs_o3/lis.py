def lis(arr):
    """
    Returns the length of the longest increasing subsequence in the array.
    Uses a binary search approach (Patience Sorting algorithm).
    """
    if not arr:
        return 0

    # 'tails' will store the smallest tail for all increasing subsequences of given lengths.
    tails = []

    # Import bisect for binary search
    import bisect

    for num in arr:
        # Find insertion point: first index in tails where num can be placed
        idx = bisect.bisect_left(tails, num)
        # If num is greater than all tails, extend the list
        if idx == len(tails):
            tails.append(num)
        else:
            # Otherwise, replace to maintain minimal tail values
            tails[idx] = num

    return len(tails)

# For testing purposes
if __name__ == '__main__':
    test_cases = [
        ([4, 1, 5, 3, 7, 6, 2], 3),
        # Additional test cases based on feedback, note that feedback expected values are off by one
        # But here, we assume standard definition of longest increasing subsequence
        ([10, 20, 11, 32, 22, 48, 43], 4),
        ([4, 2, 1], 1),
        ([1, 2, 3, 4, 5, 6], 6),
        ([], 0),
        ([5], 1),
        ([5, 4, 3, 2, 1], 1)
    ]

    for i, (inp, expected) in enumerate(test_cases, 1):
        result = lis(inp)
        print(f"Test case {i}: Input: {inp}, Expected: {expected}, Got: {result}")
