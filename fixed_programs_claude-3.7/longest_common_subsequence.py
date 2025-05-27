# Fixed Program: longest_common_subsequence (Claude 3.7 Sonnet)
# Bug Classification: Incorrect variable
# Bug Description: In the recursive call when a[0] == b[0], the function only removes the first character from string 'a' while keeping string 'b' unchanged. This causes the matching character in 'b' to be reconsidered in subsequent recursive calls, leading to incorrect results.
# Fixed on: 2025-05-27 22:50:59
# LLM Used: Claude 3.7 Sonnet
# 
# Original bug was classified as: Incorrect variable
# This indicates: In the recursive call when a[0] == b[0], the function only removes the first character from string 'a' while keeping string 'b' unchanged. This causes the matching character in 'b' to be reconsidered in subsequent recursive calls, leading to incorrect results.

def longest_common_subsequence(a, b):
    if not a or not b:
        return ''

    elif a[0] == b[0]:
        return a[0] + longest_common_subsequence(a[1:], b[1:])

    else:
        return max(
            longest_common_subsequence(a, b[1:]),
            longest_common_subsequence(a[1:], b),
            key=len
        )


 
"""
Longest Common Subsequence


Calculates the longest subsequence common to the two input strings. (A subsequence is any sequence of letters in the same order
they appear in the string, possibly skipping letters in between.)

Input:
    a: The first string to consider.
    b: The second string to consider.

Output:
    The longest string which is a subsequence of both strings. (If multiple subsequences of equal length exist, either is OK.)

Example:
    >>> longest_common_subsequence('headache', 'pentadactyl')
    'eadac'
"""