def square_generator(n: int) -> int:
    for i in range(1, n + 1):
        yield i * i

n = int(input())
for i in square_generator(n):
    print(i)