import os

def delete_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)
        return f"{file_path} has been deleted."
    else:
        return False
    
n = input("Enter the file path to delete")