def trapezoid_area(h, b1, b2):
    area = h * (b1 + b2) / 2
    print("Area of the trapezoid:", area)

height = float(input("Height: "))
base1 = float(input("Base, first value: "))
base2 = float(input("Base, second value: "))
trapezoid_area(height, base1, base2)