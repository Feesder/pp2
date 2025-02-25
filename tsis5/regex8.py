import re

with open('row.txt', 'r', encoding="utf-8") as txt:
    text = txt.read()
    result = re.findall(r'[A-Z][^A-Z]*', text)
    print("Split result:", result)