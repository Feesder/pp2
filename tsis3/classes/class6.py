def is_prime(x: int) -> bool:
    if x == 1:
        return False

    for i in range(2, x):
        if x % i == 0:
            return False

    return True


numbers = [i for i in range(1, 101)]
print(list(filter(lambda x: is_prime(x), numbers)))