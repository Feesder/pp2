def isPalindrome(word: str) -> bool:
    res = True
    for i in range(len(word) // 2):
        if word[i] != word[len(word) - i - 1]:
            res = False

    return res


word = str(input())
print(isPalindrome(word))