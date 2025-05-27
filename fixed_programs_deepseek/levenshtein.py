# Fixed Program: levenshtein (DeepSeek)
# Bug Classification: Incorrect variable
# Bug Description: The line `levenshtein(source[1:], target[1:])` was redundant in the `min` function call, as the substitution case is already handled in the `elif` condition. This led to an incorrect calculation of the Levenshtein distance.
# Fixed on: 2025-05-27 12:52:55
# LLM Used: DeepSeek
# 
# Original bug was classified as: Incorrect variable
# This indicates: The line `levenshtein(source[1:], target[1:])` was redundant in the `min` function call, as the substitution case is already handled in the `elif` condition. This led to an incorrect calculation of the Levenshtein distance.

def levenshtein(source, target):
    if source == '' or target == '':
        return len(source) or len(target)

    elif source[0] == target[0]:
        return levenshtein(source[1:], target[1:])

    else:
        return 1 + min(
            levenshtein(source,     target[1:]),
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