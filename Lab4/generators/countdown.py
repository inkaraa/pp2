def countdown(n):
    for i in range(n, -1, -1):
        yield i

n = int(input("Enter a number for countdown: "))
for number in countdown(n):
    print(number, end=" ")
print()