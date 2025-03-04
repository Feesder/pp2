import os


def generate_text_files():
    try:
        for ascii_value in range(ord('A'), ord('Z') + 1):
            letter = chr(ascii_value)
            file_name = f"test/{letter}.txt"

            with open(file_name, 'w') as file:
                file.write(f"This is the content of {file_name}.\n")

            print(f"Created file: {file_name}")
    except Exception as e:
        print(f"An error occurred: {e}")


generate_text_files()