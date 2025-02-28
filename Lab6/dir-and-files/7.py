import shutil

def copy_file(src, dst):
    shutil.copy(src, dst)

n = input("Enter the source of copy file: ")
n = input("Enter the destination of copy file: ")