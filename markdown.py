import re


def parse_underscores(curr: str):
    while m := re.match('(.*)__(.*?)__(.*)', curr):
        curr = m.group(1) + '<strong>' + m.group(2) + '</strong>' + m.group(3)
    # these are coupled - parsing __ must precede _
    while m := re.match('(.*)_(.*?)_(.*)', curr):
        curr = m.group(1) + '<em>' + m.group(2) + '</em>' + m.group(3)
    return curr

def parse(markdown: str):
    lines = markdown.split('\n')
    res = ''
    in_list = False
    for line in lines:
        line = parse_underscores(line)
        nonheader = line.lstrip('#')
        header_len = len(line) - len(nonheader)
        if header_len in range(1, 7):
            line = f'<h{header_len}>' + nonheader + f'</h{header_len}>'
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
