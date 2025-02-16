import math

def regular_polygon_area(n_sides, side_len):
    if n_sides < 3:
        print("A polygon must have at least 3 sides.")
        return
    area = (n_sides * side_len ** 2) / (4 * math.tan(math.pi / n_sides))
    print(f"The area of the polygon is: {area:.2f}")

num_sides = int(input("Input number of sides: "))
side_length = float(input("Input the length of a side: "))

regular_polygon_area(num_sides, side_length)