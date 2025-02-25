import re

with open('row.txt', 'r', encoding="utf-8") as txt:
    pattern = r'[A-Z][a-z]+'
    test_string = txt.read()
    matches = re.findall(pattern, test_string)
    print("Matches:", matches)