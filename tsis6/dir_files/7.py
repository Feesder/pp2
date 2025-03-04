def copy_file(source_path: str, destination_path: str):
    try:
        with open(source_path, 'r') as source_file:
            contents = source_file.read()

        with open(destination_path, 'w') as destination_file:
            destination_file.write(contents)

        print(f"Contents of '{source_path}' have been copied to '{destination_path}' successfully.")
    except FileNotFoundError:
        print(f"Error: The file '{source_path}' does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")


source_path = ""
destination_path = ""
copy_file(source_path, destination_path)