# Fixed Program: levenshtein (Claude 3.5 Sonnet)
# Bug Classification: Missing arithmetic expression
# Bug Description: The code incorrectly adds 1 to the Levenshtein distance calculation when characters match, which should not incur any cost. This causes the algorithm to count matching characters as edit operations, resulting in incorrect distance calculations.
# Fixed on: 2025-05-27 13:41:50
# LLM Used: Claude 3.5 Sonnet
# 
# Original bug was classified as: Missing arithmetic expression
# This indicates: The code incorrectly adds 1 to the Levenshtein distance calculation when characters match, which should not incur any cost. This causes the algorithm to count matching characters as edit operations, resulting in incorrect distance calculations.

def levenshtein(source, target):
    if source == '' or target == '':
        return len(source) or len(target)

    elif source[0] == target[0]:
        return levenshtein(source[1:], target[1:])

    else:
        return 1 + min(
            levenshtein(source,     target[1:]),
            levenshtein(source[1:], target[1:]),
            levenshtein(source[1:], target)
        )
 
"""
Levenshtein Distance


Calculates the Levenshtein distance between two strings.  The Levenshtein distance is defined as the minimum amount of single-character edits (either removing a character, adding a character, or changing a character) necessary to transform a source string into a target string.

Input:
    source: The string you begin with.
    target: The string to transform into.

Output:
    The Levenshtein distance between the source and target.

Example:
    electron can be transformed into neutron by removing the e, turning the l into n, and turning the c into u.
    >>> levenshtein(electron, neutron)
    3
"""