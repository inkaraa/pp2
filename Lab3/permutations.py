from itertools import permutations

def print_permutations(s):
    perm_set = set(permutations(s))
    for perm in perm_set:
        print(''.join(perm))


user_str = "ABC"
print_permutations(user_str)