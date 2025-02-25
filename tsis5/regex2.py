import re

with open('row.txt', 'r', encoding="utf-8") as txt:
    pattern = r'ab{2,3}'
    test_strings = txt.read().split(' ')
    for string in test_strings:
        if re.match(pattern, string):
            print(f"Matched: {string}")