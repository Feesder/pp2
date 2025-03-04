def count_lines_in_file(file_path: str):
    try:
        with open(file_path, 'r') as file:
            line_count = sum(1 for line in file)
        return line_count
    except FileNotFoundError:
        print(f"The file '{file_path}' does not exist.")
        return None

file_path = "1.py"
line_count = count_lines_in_file(file_path)
print(f"The file '{file_path}' contains {line_count} lines.")