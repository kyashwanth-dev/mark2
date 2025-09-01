# convert.py
from lexerNew import tokenize

with open("sample.12e") as f:
    code = f.read()

tokens = tokenize(code)

for token in tokens:
    print(f"{token.line}:{token.column} [{token.type}] → {token.value}")
                