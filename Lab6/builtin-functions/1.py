import math
list = input("Enter the list : ").split(" ")
nlist = []
for n in list:
    list.append(int(n))
print(math.prod(nlist))