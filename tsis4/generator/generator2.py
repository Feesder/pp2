def even_numbers(n: int) -> int:
    for i in range(1, n + 1):
        if i % 2 == 0:
            yield i


n = int(input())
for i in even_numbers(n):
    print(i)