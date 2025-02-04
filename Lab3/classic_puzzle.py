def solve(num_heads, num_legs):
    y = (num_legs - 2 * num_heads) // 2
    x = num_heads - y
    return x, y

num_heads=35
num_legs=94
answer=solve(num_heads, num_legs)
print(answer)

