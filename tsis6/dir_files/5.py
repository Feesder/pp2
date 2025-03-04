def write_list_to_file(file_path: str, data_list: list[str]):
    try:
        with open(file_path, 'w') as file:
            for item in data_list:
                file.write(f"{item}\n")
        print(f"The list has been written to '{file_path}' successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")

data_list = ["Apple", "Banana", "Cherry", "Date", "Elderberry"]
file_path = "output.txt"

write_list_to_file(file_path, data_list)