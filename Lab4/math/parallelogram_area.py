def parallelogram_area(b, h):
    area = b * h
    print(f"Area of parallelogram: {area:.1f}")

base = float(input("\nLength of base: "))
height = float(input("Height of parallelogram: "))

parallelogram_area(base, height)