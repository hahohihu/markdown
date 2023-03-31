import re
from typing import Optional

"""
Refactoring notes in broad strokes:
1. Got rid of major duplication
2. Extracted some functions
3. Converted boolean state into implicit program state
4. Generalized the header parsing (of dubious utility admittedly)
5. Simplified control flow
6. Added some type hints

Non-refactoring:
1. Fixed a bug in the original code where only one pair of underscores could be correctly parsed
"""

def parse_underscores(curr: str) -> str:
    while m := re.match('(.*)__(.+?)__(.*)', curr):
        curr = m.group(1) + '<strong>' + m.group(2) + '</strong>' + m.group(3)
    # these are coupled - parsing __ must precede _
    while m := re.match('(.*)_(.+?)_(.*)', curr):
        curr = m.group(1) + '<em>' + m.group(2) + '</em>' + m.group(3)
    return curr


def parse_header(curr: str) -> Optional[str]:
    if m := re.match(r'(#+) (.*)', curr):
        header_size = len(m.group(1))
        if header_size <= 6:
            return f'<h{header_size}>{m.group(2)}</h{header_size}>'
    return None


def parse(markdown: str) -> str:
    lines = markdown.split('\n')
    res = ''
    in_list = False
    for line in lines:
        line = parse_underscores(line)
        if header := parse_header(line):
            line = header
        elif m := re.match(r'\* (.*)', line):
            line = f'<li>{m.group(1)}</li>'
            if not in_list:
                in_list = True
                line = '<ul>' + line
        else:
            line = '<p>' + line + '</p>'
            if in_list:
                line = '</ul>' + line
                in_list = False
        res += line
    if in_list:
        res += '</ul>'
    return res
