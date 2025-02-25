import re

with open('row.txt', 'r', encoding="utf-8") as txt:
    pattern = r'[A-Z][a-z]+'
    test_string = txt.read()
    result = re.sub(r'_([a-z])', lambda match: match.group(1).upper(), test_string)
    print(result)