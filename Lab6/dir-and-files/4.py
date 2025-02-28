def count_lines(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return sum(1 for _ in file)
    
n = input("Enter the file path: ")
print(count_lines(n))