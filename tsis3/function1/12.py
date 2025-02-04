def histogram(numbers: list[int]) -> str:
    res = ''
    for i in range(len(numbers)):
        for j in range(numbers[i]):
            res += '*'

        res += '\n'

    return res

numbers = list(map(int, input().split(' ')))
print(histogram(numbers))