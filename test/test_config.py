from unittest.mock import patch
import pytest

from pkvid.config import (
    ConfigInvalidException,
    ConfigNotFoundException,
    process_config,
    parse_string_to_dict,
)


def test_process_config_invalid_file():
    invalid_filename = "this_file_doesnt_exist"
    with pytest.raises(ConfigNotFoundException):
        process_config(invalid_filename)


@patch("os.path.exists", return_value=True)
@patch("pkvid.config.get_file_as_string", return_value="hello")
@patch("pkvid.config.parse_string_to_dict", return_value="hello")
def test_process_config_valid(
    mock_parse_string_to_dict, mock_get_file_as_string, mock_exists
):
    valid_filename = "this_file_is_valid"
    process_config(valid_filename)
    mock_get_file_as_string.assert_called_with(valid_filename)
    mock_parse_string_to_dict.assert_called_with("hello")


def test_parse_config_invalid():
    invalid_config = """not: even: valid: yaml"""
    with pytest.raises(ConfigInvalidException):
        parse_string_to_dict(invalid_config)

def test_parse_config_json():
    json_config = '{"json":"config"}'
    config = parse_string_to_dict(json_config)
    assert config['json'] == 'config'

def test_parse_config_yaml():
    json_config = 'yaml: "config"'
    config = parse_string_to_dict(json_config)
    assert config['yaml'] == 'config'
