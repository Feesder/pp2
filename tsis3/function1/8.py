def spy_game(nums: list[int]) -> bool:
    string = "007"
    res = ""

    for i in range(len(nums)):
        if nums[i] == 0 or nums[i] == 7:
            res += str(nums[i])

    if res == string:
        return True
    else:
        return False

print(spy_game([1,2,4,0,0,7,5])) # --> True
print(spy_game([1,0,2,4,0,5,7])) # --> True
print(spy_game([1,7,2,0,4,5,0])) # --> False