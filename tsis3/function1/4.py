from math import sqrt

arr = [i for i in range(1, 101)]

def filter_prime(numbers: list[int]) -> list[int]:
    res = []
    for i in range(len(numbers)):
        b = True
        for j in range(2, int(sqrt(numbers[i]) + 1)):
            if arr[i] % j == 0:
                b = False
                break
        if b and arr[i] != 1:
            res.append(numbers[i])

    return res

print(filter_prime(arr))