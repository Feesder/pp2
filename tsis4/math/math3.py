import math

sides = int(input("Input number of sides: "))
length = float(input("Input the length of a side: "))

print(f"The area of the polygon is: {math.ceil((sides * length**2) / 4 * math.tan(math.pi / sides))}")