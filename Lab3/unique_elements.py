def unique_elements(lst):
    unique_list = []
    for item in lst:
        if item not in unique_list:
            unique_list.append(item)
    return unique_list

numbers = [1, 2, 2, 3, 4, 4, 5]
print(unique_elements(numbers))