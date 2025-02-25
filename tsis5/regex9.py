import re

with open('row.txt', 'r', encoding="utf-8") as txt:
    text = txt.read()
    result = re.sub(r'(?<!^)([A-Z])', r' \1', text)
    print("Result:", result)