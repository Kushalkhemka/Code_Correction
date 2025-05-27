# Fixed Program: wrap (Claude 3.7 Sonnet)
# Bug Classification: Missing line
# Bug Description: The function is missing a crucial line to add the remaining text to the lines list. The current implementation only appends text segments that are wrapped due to exceeding the column limit, but it doesn't add the final segment of text when it's shorter than the column limit. This means if there's any text remaining after the while loop that's shorter than 'cols', it will be ignored completely in the final output.
# Fixed on: 2025-05-27 23:04:01
# LLM Used: Claude 3.7 Sonnet
# 
# Original bug was classified as: Missing line
# This indicates: The function is missing a crucial line to add the remaining text to the lines list. The current implementation only appends text segments that are wrapped due to exceeding the column limit, but it doesn't add the final segment of text when it's shorter than the column limit. This means if there's any text remaining after the while loop that's shorter than 'cols', it will be ignored completely in the final output.

def wrap(text, cols):
    lines = []
    while len(text) > cols:
        end = text.rfind(' ', 0, cols + 1)
        if end == -1:
            end = cols
        line, text = text[:end], text[end:]
        lines.append(line)
    
    lines.append(text)  # Add the remaining text
    return lines

""" 
Wrap Text

Given a long string and a column width, break the string on spaces into a list of lines such that each line is no longer than the column width.

Input:
    text: The starting text.
    cols: The target column width, i.e. the maximum length of any single line after wrapping.

Precondition:
    cols > 0.

Output:
    An ordered list of strings, each no longer than the column width, such that the concatenation of the strings returns the original text,
and such that no word in the original text is broken into two parts unless necessary.  The original amount of spaces are preserved (e.g. spaces
at the start or end of each line aren't trimmed.),Wrapping Text
"""