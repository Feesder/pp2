def check_all_true(elements):
    return all(elements)

tuple1 = (True, True, True)
tuple2 = (True, False, True)
tuple3 = ()

print(f"All elements in {tuple1} are True: {check_all_true(tuple1)}")
print(f"All elements in {tuple2} are True: {check_all_true(tuple2)}")
print(f"All elements in {tuple3} are True: {check_all_true(tuple3)}")