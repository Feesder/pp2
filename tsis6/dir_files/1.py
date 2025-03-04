import os

def list_directories(path: str):
    print("Directories:")
    for item in os.listdir(path):
        if os.path.isdir(os.path.join(path, item)):
            print(item)

def list_files(path: str):
    print("\nFiles:")
    for item in os.listdir(path):
        if os.path.isfile(os.path.join(path, item)):
            print(item)

def list_all(path: str):
    print("\nAll items (directories and files):")
    for item in os.listdir(path):
        print(item)

path = ".."

list_directories(path)
list_files(path)
list_all(path)