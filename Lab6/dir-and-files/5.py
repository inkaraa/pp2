def write_list_to_file(file_path, data_list):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines("\n".join(data_list))

n = input("Enter file path: ")
m = list(input("Enter the list: ").split(" "))
write_list_to_file(n, m)
