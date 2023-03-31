import re

def format_bold(curr):
    m = re.match('(.*)__(.*)__(.*)', curr)
    if m:
        curr = m.group(1) + '<strong>' + m.group(2) + '</strong>' + m.group(3)
    return curr

def format_italic(curr):
    m = re.match('(.*)_(.*)_(.*)', curr)
    if m:
        curr = m.group(1) + '<em>' + m.group(2) + '</em>' + m.group(3)
    return curr

def format_list_item(curr):
    curr = format_bold(curr)
    curr = format_italic(curr)
    return '<li>' + curr + '</li>'

def parse(markdown):
    lines = markdown.split('\n')
    res = ''
    in_list = False
    in_list_append = False
    for line in lines:
        if re.match('###### (.*)', line) is not None:
            line = '<h6>' + line[7:] + '</h6>'
        elif re.match('##### (.*)', line) is not None:
            line = '<h5>' + line[6:] + '</h5>'
        elif re.match('#### (.*)', line) is not None:
            line = '<h4>' + line[5:] + '</h4>'
        elif re.match('### (.*)', line) is not None:
            line = '<h3>' + line[4:] + '</h3>'
        elif re.match('## (.*)', line) is not None:
            line = '<h2>' + line[3:] + '</h2>'
        elif re.match('# (.*)', line) is not None:
            line = '<h1>' + line[2:] + '</h1>'
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
        line = format_bold(line)
        line = format_italic(line)
        if in_list_append:
            line = '</ul>' + line
            in_list_append = False
        res += line
    if in_list:
        res += '</ul>'
    return res
