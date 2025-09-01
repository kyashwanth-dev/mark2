# lexerNew.py
import re
from collections import namedtuple

Token = namedtuple("Token", ["type", "value", "line", "column"])

token_specs = [
    ('TAG_OPEN',     r'\.\.[a-zA-Z]+\.\.'),            # ..led.., ..battery..
    ('TAG_CLOSE',    r';\.\.[a-zA-Z]+\.\.;'),          # ;..led..;
    ('COMMENT_SINGLE', r'//[^\n]*'),                   # // comment
    ('COMMENT_MULTI_START', r'<'),                     # < multiline start
    ('COMMENT_MULTI_END',   r'>'),                     # > multiline end
    ('STRING',       r'"[^"]*"'),                      # "quoted strings"
    ('KEYWORD',      r'\b(name|terminal|male|female|pos|neg|with|pairTo|attach|dig|print|state|out|zero|ntr|ON|OFF)\b'),
    ('IDENTIFIER',   r'\b[a-zA-Z_][a-zA-Z0-9_]*\b'),    # variable names
    ('NUMBER',       r'\b\d+\b'),                      # numbers
    ('COMMA',        r','),                            # comma
    ('WHITESPACE',   r'[ \t]+'),                       # spaces/tabs
    ('NEWLINE',      r'\n'),                           # newline
    ('MISMATCH',     r'.'),                            # anything else
]

def tokenize(code):
    tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specs)
    get_token = re.compile(tok_regex).match
    line_num = 1
    pos = line_start = 0
    tokens = []

    inside_multiline = False

    while pos < len(code):
        m = get_token(code, pos)
        if not m:
            raise SyntaxError(f'Unexpected character {code[pos]!r} on line {line_num}')
        kind = m.lastgroup
        value = m.group()

        if kind == 'NEWLINE':
            line_start = pos + 1
            line_num += 1
        elif kind == 'WHITESPACE':
            pass
        elif kind == 'COMMENT_SINGLE':
            pass
        elif kind == 'COMMENT_MULTI_START':
            inside_multiline = True
        elif kind == 'COMMENT_MULTI_END':
            inside_multiline = False
        elif inside_multiline:
            pass
        elif kind != 'MISMATCH':
            column = pos - line_start
            tokens.append(Token(kind, value, line_num, column))
        else:
            raise RuntimeError(f'Unexpected token: {value!r} at line {line_num}')

        pos = m.end()

    return tokens
