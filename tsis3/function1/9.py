import math

def calculateVolumeOfSphere(radius: float) -> float:
    return 4 / 3 * (radius ** 3) * math.pi


r = float(input())
print(calculateVolumeOfSphere(r))
