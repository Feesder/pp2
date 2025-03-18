def is_palindrome(input_string: str) -> bool:
    cleaned_string = input_string.replace(" ", "").lower()
    return cleaned_string == cleaned_string[::-1]


input_string = "Mala alam"
if is_palindrome(input_string):
    print(f'"{input_string}" is a palindrome.')
else:
    print(f'"{input_string}" is not a palindrome.')