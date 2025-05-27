# Fixed Program: wrap (DeepSeek)
# Bug Classification: Missing condition
# Bug Description: The loop condition did not account for the case where the remaining text is exactly `cols` in length or less, causing the last line to be omitted from the output. This violates the requirement that the concatenation of the lines should return the original text.
# Fixed on: 2025-05-27 12:52:46
# LLM Used: DeepSeek
# 
# Original bug was classified as: Missing condition
# This indicates: The loop condition did not account for the case where the remaining text is exactly `cols` in length or less, causing the last line to be omitted from the output. This violates the requirement that the concatenation of the lines should return the original text.

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