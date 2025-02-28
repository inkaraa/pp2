import os

def path_info(path):
    if os.path.exists(path):
        return {"Directory": os.path.dirname(path), "Filename": os.path.basename(path)}
    else:
        return False
    
n = input("Enter the path: ")

print(path_info(n))