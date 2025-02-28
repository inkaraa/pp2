import os
def list_files_and_dirs(path="."):
    dirs = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]
    files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    return {"Directories" : dirs, "Files": files, "All" : os.listdir(path)}

n = input("Enter the path: ")
a = list_files_and_dirs(n)
print(a)