# Fixed Program: levenshtein (Claude 3.7 Sonnet)
# Bug Classification: Missing/added +1
# Bug Description: The Levenshtein distance algorithm incorrectly added a penalty (+1) when characters match. When characters are the same, we should simply recurse on the remaining substrings without adding any cost. The original implementation would produce incorrect distances by counting matching characters as edits.
# Fixed on: 2025-05-27 22:49:54
# LLM Used: Claude 3.7 Sonnet
# 
# Original bug was classified as: Missing/added +1
# This indicates: The Levenshtein distance algorithm incorrectly added a penalty (+1) when characters match. When characters are the same, we should simply recurse on the remaining substrings without adding any cost. The original implementation would produce incorrect distances by counting matching characters as edits.

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