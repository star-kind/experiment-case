import os


def recursive_directory_search(relative_path, excluded_names):
    directory_list = []

    for root, dirs, files in os.walk(relative_path):
        for dir_name in dirs:
            if dir_name not in excluded_names:
                absolute_dir_path = os.path.abspath(os.path.join(root, dir_name))
                directory_list.append(absolute_dir_path)

    return directory_list


def filter_list(source_list, excluded_substrings):
    filtered_list = []

    for element in source_list:
        # check excluded_substrings.substring whether or not in source_list.element
        if all(substring not in element for substring in excluded_substrings):
            filtered_list.append(element)

    return filtered_list


def write_list_to_file(source_list, relative_path):
    with open(relative_path, "a", encoding="utf-8") as output_file:
        for element in source_list:
            output_file.write(element + "\n")


def gain_pth_file():
    relative_path = "."
    output_file = "./experiment-case.pth"
    excluded_names = ["__pycache__"]
    excluded_substrings = ["static", "templates", ".git", ".vscode"]

    directory_list = recursive_directory_search(relative_path, excluded_names)

    filtered_list = filter_list(directory_list, excluded_substrings)

    for element in filtered_list:
        print(element)

    write_list_to_file(filtered_list, output_file)


gain_pth_file()
