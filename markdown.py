import re

def parse_underscores(curr):
    while m := re.match('(.*)__(.*?)__(.*)', curr):
        curr = m.group(1) + '<strong>' + m.group(2) + '</strong>' + m.group(3)
    # these are coupled - parsing __ must precede _
    while m := re.match('(.*)_(.*?)_(.*)', curr):
        curr = m.group(1) + '<em>' + m.group(2) + '</em>' + m.group(3)
    return curr

def format_list_item(curr):
    curr = parse_underscores(curr)
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
    in_list_append = False
    for line in lines:
        header_level = count_header_level(line)
        if header_level > 0:
            line = '<h' + str(header_level) + '>' + line[header_level + 1:] + '</h' + str(header_level) + '>'
        m = re.match(r'\* (.*)', line)
        if m:
            if not in_list:
                in_list = True
                line = '<ul>' + format_list_item(m.group(1))
            else:
                line = format_list_item(m.group(1))
        else:
            if in_list:
                in_list_append = True
                in_list = False

        m = re.match('<h|<ul|<p|<li', line)
        if not m:
            line = '<p>' + line + '</p>'
        line = parse_underscores(line)
        if in_list_append:
            line = '</ul>' + line
            in_list_append = False
        res += line
    if in_list:
        res += '</ul>'
    return res
