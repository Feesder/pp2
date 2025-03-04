import os


def delete_file(file_path: str):
    if not os.path.exists(file_path):
        print(f"The file '{file_path}' does not exist.")
        return

    if not os.path.isfile(file_path):
        print(f"'{file_path}' is not a file.")
        return

    if not os.access(file_path, os.W_OK):
        print(f"No write access to the file '{file_path}'. Cannot delete.")
        return

    try:
        os.remove(file_path)
        print(f"File '{file_path}' has been deleted successfully.")
    except Exception as e:
        print(f"An error occurred while deleting the file: {e}")


file_path = input("Enter the file path to delete: ")
delete_file(file_path)