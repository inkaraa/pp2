def even_numbers_generator(n):
    for i in range(n + 1):
        if i % 2 == 0:
            yield i

n = int(input("Enter a number for even numbers generator: "))
evens = list(even_numbers_generator(n))
print(evens)