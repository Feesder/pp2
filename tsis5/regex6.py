import re

with open('row.txt', 'r', encoding="utf-8") as txt:
    text = txt.read()
    result = re.sub(r'[ ,.]', ':', text)
    print("Result:", result)