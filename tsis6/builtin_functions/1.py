from functools import reduce

def multiply_list_numbers(numbers: list[int]) -> int:
    result = reduce(lambda x, y: x * y, numbers)
    return result

numbers = [1, 2, 3, 4, 5]
result = multiply_list_numbers(numbers)
print(result)