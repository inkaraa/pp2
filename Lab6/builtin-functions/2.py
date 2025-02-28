s = input("Enter a string : ")
def count_case(s):
    upper_count = sum(1 for c in s if c.isupper())
    lower_count = sum(1 for c in s if c.islower())
    return f"Uppers : {upper_count}, Lowers : {lower_count}"
print(count_case(s))