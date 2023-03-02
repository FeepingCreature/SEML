#!/usr/bin/env python3
import sys
import re

p = re.compile('(?P<indent> *)(' +
               '(?P<obj_key>[\w_-]+):(?P<obj_value>.+)?' +
               '|(?P<array_entry>-(?P<array_value>.+)?)' +
               '|(?P<comment>#.*)' +
               '|(?P<empty_line>)' +
               ')')

lines = [line.rstrip('\n') for line in sys.stdin]
def process(min_indent = -1):
    global lines
    expected_indent = None
    result = None
    while lines:
        line = lines[0]
        m = p.fullmatch(line)
        assert m, "line failed to parse: '" + line + "'"

        if m.group('comment') is not None or m.group('empty_line') is not None:
            lines = lines[1:]
            continue

        indent = len(m.group('indent'))
        if m.group('array_entry'):
            indent += 1

        if expected_indent:
            if indent < expected_indent:
                break
            assert indent == expected_indent, "wrong indent in '" + line + "'"
        else:
            assert indent > min_indent, "unexpected dedent in '" + line + "'"
            expected_indent = indent
        lines = lines[1:]

        if m.group('array_entry'):
            if result:
                assert isinstance(result, list)
            else:
                result = []
            if m.group('array_value'):
                result.append(m.group('array_value').strip())
            else:
                result.append(process(expected_indent))
        elif m.group('obj_key'):
            if result:
                assert not isinstance(result, list)
            else:
                result = {}
            if m.group('obj_value'):
                result[m.group('obj_key')] = m.group('obj_value').strip()
            else:
                result[m.group('obj_key')] = process(expected_indent)
    return result

print(process())
