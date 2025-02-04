from itertools import permutations

word = str(input())
result = permutations(word)

for i in result:
    for j in i:
        print(j, end="")
    print("")