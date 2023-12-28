import json
import os

import yaml

from pkvid.project import ProjectConfig


class ConfigNotFoundException(Exception):
    pass
class ConfigInvalidException(Exception):
    pass

def get_file_as_string(filename: str):
    with open(filename, "r") as file:
        contents = file.read()
    return contents

def get_config(filename: str):
    if os.path.exists(filename):
        contents = get_file_as_string(filename)
        config_dict = parse_string_to_dict(contents)
        config = ProjectConfig(**config_dict)
        return config
    else:
        raise ConfigNotFoundException(f"File not found: {filename}")

def parse_string_to_dict(contents: str):
    # Try parsing JSON first
    try:
        config_dict = json.loads(contents)
    except:
        config_dict = None
    if config_dict is None:
        # Try yaml now
        try:
            config_dict = yaml.safe_load(contents)
        except:
            config_dict = None
        if config_dict is None:
            # If nothing has worked yet, we have a problem
            raise ConfigInvalidException()
        else:
            # Return valid config from YAML
            return config_dict
    else:
        # Return valid config from JSON
        return config_dict
