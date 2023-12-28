import os


def get_file_as_string(filename: str):
    with open(filename, "r") as file:
        contents = file.read()
    return contents

def process_config(filename: str):
    if os.path.exists(filename):
        contents = get_file_as_string(filename)
        config = parse_config_from_string(contents)
    else:
        raise ValueError(f"File not found: {filename}")

def parse_config_from_string(contents: str):
    pass
