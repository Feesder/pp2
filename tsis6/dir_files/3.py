import os


def check_path_and_extract_info(path: str):
    if os.path.exists(path):
        print(f"The path '{path}' exists.")

        directory = os.path.dirname(path)
        print(f"Directory portion: {directory}")

        filename = os.path.basename(path)
        print(f"Filename portion: {filename}")
    else:
        print(f"The path '{path}' does not exist.")


path = "1.py"
check_path_and_extract_info(path)