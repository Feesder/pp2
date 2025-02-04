def has_33(nums: list[int]) -> bool:
    res = False
    for i in range(1, len(nums)):
        if nums[i - 1] == nums[i] == 3:
            res = True

    return res


print(has_33([1, 3, 3])) # → True
print(has_33([1, 3, 1, 3])) # → False
print(has_33([3, 1, 3])) # → False