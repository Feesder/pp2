words = str(input())
arr = words.split(" ")

for i in range(len(arr) - 1, -1, -1):
    print(arr[i], end=" ")