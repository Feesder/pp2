def uniqueList(elements: list[int]) -> list[int]:
    res = []
    for i in range(len(elements)):
        unique = True
        for j in range(i + 1, len(elements)):
            if elements[i] == elements[j]:
                unique = False

        if unique:
            res.append(elements[i])

    return res

elements = input().split(' ')
for i in range(len(elements)):
    elements[i] = int(elements[i])

print(uniqueList(elements))