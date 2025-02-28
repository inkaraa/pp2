import os
n = input("Enter the path: ")

def check_access(path):
    return {
        "Exists" : os.path.exists(path),
        "Readable" : os.access(path, os.R_OK),
        "Writable" : os.access(path, os.W_OK),
        "Executable" : os.access(path, os.EX_OK)
    }

print(check_access(n))