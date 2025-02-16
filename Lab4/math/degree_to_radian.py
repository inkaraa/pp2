import math

def degree_to_radian(n):
    radian = math.radians(n)
    print(f"Output radian: {radian:.6f}")

deg = float(input("Enter degree: "))
degree_to_radian(deg)