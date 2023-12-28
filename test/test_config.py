import pytest

from pkvid.config import process_config


def test_process_config_invalid_file():
    invalid_filename = 'this_file_doesnt_exist'
    with pytest.raises(ValueError):
        process_config(invalid_filename)
