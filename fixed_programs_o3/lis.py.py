def lis(arr):
    # This function computes the length of the longest increasing subsequence (LIS) in arr.
    # It uses a dictionary 'ends' that maps subsequence lengths (1-indexed) to the index in arr
    # of the smallest possible tail value for a subsequence of that length.
    # The invariant is that for lengths 1 through 'longest', ends[length] is always defined.
    
    if not arr:
        return 0
    
    # Initialize the dictionary and the length of the longest subsequence found so far.
    ends = {}  # key: subsequence length, value: index in arr
    longest = 0

    for i, val in enumerate(arr):
        # Find the maximum subsequence length 'length' such that the tail of that subsequence is less than val
        length = 0
        for j in range(1, longest + 1):
            if arr[ends[j]] < val:
                # Update 'length' to be the maximum valid subsequence length that can be extended
                length = max(length, j)
        
        # Instead of directly accessing ends[length+1] (which might risk a KeyError if the invariant is broken), 
        # we explicitly check if the key exists. This adds robustness for future modifications.
        
        # If we can extend the longest subsequence, or if we found a better candidate tail for an existing subsequence length:
        if length == longest:
            # When length == longest, we always extend by setting ends[length+1] to the current index
            ends[length + 1] = i
            longest += 1
        elif (length + 1 not in ends) or (val < arr[ends[length + 1]]):
            # For existing subsequence of length (length+1), replace the tail if val is smaller
            ends[length + 1] = i
    
    return longest

# Example test run
if __name__ == '__main__':
    # Test case: [4, 1, 5, 3, 7, 6, 2]
    test_array = [4, 1, 5, 3, 7, 6, 2]
    print("Length of LIS:", lis(test_array))
