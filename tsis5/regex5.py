import re

with open('row.txt', 'r', encoding="utf-8") as txt:
    pattern = r'a.*b$'
    test_strings = txt.read().split(' ')
    print(test_strings)
    for string in test_strings:
        if re.match(pattern, string):
            print(f"Matched: {string}")