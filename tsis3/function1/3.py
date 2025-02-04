heads = int(input())
legs = int(input())

def solve(heads: int, legs: int) -> str:
    x = 2 * heads - legs / 2
    y = legs / 2 - heads

    return f"chickens: {int(x)}, rabbits: {int(y)}"

print(solve(heads, legs))
