import re

def parse_underscores(curr):
    while m := re.match('(.*)__(.*?)__(.*)', curr):
        curr = m.group(1) + '<strong>' + m.group(2) + '</strong>' + m.group(3)
    # these are coupled - parsing __ must precede _
    while m := re.match('(.*)_(.*?)_(.*)', curr):
        curr = m.group(1) + '<em>' + m.group(2) + '</em>' + m.group(3)
    return curr

def format_list_item(curr):
    return '<li>' + curr + '</li>'

# returns header level - 0 if it isn't a header
def count_header_level(line):
    level = len(line) - len(line.lstrip('#'))
    # level > 6 is invalid so treat it as a non-header
    return level % 7

def parse(markdown):
    lines = markdown.split('\n')
    res = ''
    in_list = False
    for line in lines:
        line = parse_underscores(line)
        header_level = count_header_level(line)
        if header_level > 0:
            line = '<h' + str(header_level) + '>' + line[header_level + 1:] + '</h' + str(header_level) + '>'
        elif m := re.match(r'\* (.*)', line):
            line = format_list_item(m.group(1))
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
