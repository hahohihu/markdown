import re
from typing import Optional


def parse_underscores(curr: str) -> str:
    while m := re.match('(.*)__(.*?)__(.*)', curr):
        curr = m.group(1) + '<strong>' + m.group(2) + '</strong>' + m.group(3)
    # these are coupled - parsing __ must precede _
    while m := re.match('(.*)_(.*?)_(.*)', curr):
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
