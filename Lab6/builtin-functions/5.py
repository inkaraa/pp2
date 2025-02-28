def all_true(t):
    return all(t)

n = tuple(input("Enter the tuple: ").split(" "))
print(all_true(n))