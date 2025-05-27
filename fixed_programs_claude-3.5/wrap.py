# Fixed Program: wrap (Claude 3.5 Sonnet)
# Bug Classification: Missing line
# Bug Description: The code fails to append the remaining text when its length becomes less than or equal to the column width. This causes the final portion of text to be lost in the output.
# Fixed on: 2025-05-27 13:42:08
# LLM Used: Claude 3.5 Sonnet
# 
# Original bug was classified as: Missing line
# This indicates: The code fails to append the remaining text when its length becomes less than or equal to the column width. This causes the final portion of text to be lost in the output.

def wrap(text, cols):
    lines = []
    while len(text) > cols:
        end = text.rfind(' ', 0, cols + 1)
        if end == -1:
            end = cols
        line, text = text[:end], text[end:]
        lines.append(line)
    
    if text:
        lines.append(text)
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