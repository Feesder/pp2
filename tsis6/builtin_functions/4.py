import time
import math

def calculate_square_root_after_delay(number: int, delay_ms: int) -> float:
    delay_seconds = delay_ms / 1000.0
    time.sleep(delay_seconds)
    return math.sqrt(number)

number = 25100
delay_ms = 2123
result = calculate_square_root_after_delay(number, delay_ms)
print(f"Square root of {number} after {delay_ms} milliseconds is {result}")