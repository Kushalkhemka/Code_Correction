# Fixed Program: lcs_length (Claude 3.5 Sonnet)
# Bug Classification: Missing line
# Bug Description: The code was not properly using the dynamic programming approach for longest common substring by failing to initialize the DP table with 0s and incorrectly accessing previous diagonal values.
# Fixed on: 2025-05-27 13:42:10
# LLM Used: Claude 3.5 Sonnet
# 
# Original bug was classified as: Missing line
# This indicates: The code was not properly using the dynamic programming approach for longest common substring by failing to initialize the DP table with 0s and incorrectly accessing previous diagonal values.

def lcs_length(s, t):
    if not s or not t:
        return 0
        
    # Create DP table initialized with 0s
    dp = [[0] * (len(t) + 1) for _ in range(len(s) + 1)]
    max_length = 0

    # Fill the DP table
    for i in range(1, len(s) + 1):
        for j in range(1, len(t) + 1):
            if s[i-1] == t[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
                max_length = max(max_length, dp[i][j])

    return max_length


"""
Longest Common Substring
longest-common-substring

Input:
    s: a string
    t: a string

Output:
    Length of the longest substring common to s and t

Example:
    >>> lcs_length('witch', 'sandwich')
    2
    >>> lcs_length('meow', 'homeowner')
    4
"""