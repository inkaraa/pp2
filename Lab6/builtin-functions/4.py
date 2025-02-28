import math, time

def delayed_sqrt(number, miliseconds):
    time.sleep(miliseconds/1000)
    print(f"Square root of {number} after {miliseconds} miliseconds is {math.sqrt(number)}")

num = int(input("Enter the number : "))
ms = int(input("Enter the miliseconds : "))
delayed_sqrt(num, ms)