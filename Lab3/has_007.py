def has_007(nums):
    code = [0, 0, 7]
    for n in nums:
        if len(code) > 0 and n == code[0]:
            code.pop(0)
    return len(code) == 0


print(has_007([1,2,4,0,0,7,5]))
print(has_007([1,0,2,4,0,5,7]))
print(has_007([1,7,2,0,4,5,0]))