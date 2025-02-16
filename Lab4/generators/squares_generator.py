def squares_generator(n):
    for i in range(n + 1):
        yield i ** 2

N = int(input("N :"))
for square in squares_generator(N):
    print(square, end=" ")
print()