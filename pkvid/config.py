import os


def process_config(filename: str):
    if os.path.exists(filename):
        print("Processing: " + filename)
    else:
        raise ValueError(f"File not found: {filename}")
