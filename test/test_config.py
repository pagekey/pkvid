from unittest.mock import patch
import pytest

from pkvid.config import process_config


def test_process_config_invalid_file():
    invalid_filename = 'this_file_doesnt_exist'
    with pytest.raises(ValueError):
        process_config(invalid_filename)

@patch('os.path.exists', return_value=True)
@patch('pkvid.config.get_file_as_string', return_value='hello')
@patch('pkvid.config.parse_config_from_string', return_value='hello')
def test_process_config_valid(mock_parse_config_from_string, mock_get_file_as_string, mock_exists):
    valid_filename = 'this_file_is_valid'
    process_config(valid_filename)
    mock_get_file_as_string.assert_called_with(valid_filename)
    mock_parse_config_from_string.assert_called_with('hello')
