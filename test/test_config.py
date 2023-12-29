from unittest.mock import patch
import pytest

from pkvid.config import (
    ConfigInvalidException,
    ConfigNotFoundException,
    get_config,
    parse_string_to_dict,
)


def test_get_config_invalid_file():
    invalid_filename = "this_file_doesnt_exist"
    with pytest.raises(ConfigNotFoundException):
        get_config(invalid_filename)


@patch("pkvid.config.ProjectConfig", return_value="the_config")
@patch("pkvid.config.parse_string_to_dict", return_value={"hello": "hello"})
@patch("pkvid.config.get_file_as_string", return_value="hello")
@patch("os.path.exists", return_value=True)
def test_get_config_valid(
    mock_exists,
    mock_get_file_as_string,
    mock_parse_string_to_dict,
    mock_project_config_class
):
    valid_filename = "this_file_is_valid"
    config = get_config(valid_filename)
    mock_get_file_as_string.assert_called_with(valid_filename)
    mock_parse_string_to_dict.assert_called_with("hello")
    mock_project_config_class.assert_called_with(**{"hello": "hello"})
    assert config == "the_config"


def test_parse_string_to_dict_invalid():
    invalid_config = """not: even: valid: yaml"""
    with pytest.raises(ConfigInvalidException):
        parse_string_to_dict(invalid_config)

def test_parse_string_to_dict_json():
    json_config = '{"json":"config"}'
    config = parse_string_to_dict(json_config)
    assert config['json'] == 'config'

def test_parse_string_to_dict_yaml():
    json_config = 'yaml: "config"'
    config = parse_string_to_dict(json_config)
    assert config['yaml'] == 'config'
