import pytest
from modules.file_integrity import verify_file_hash

@pytest.mark.parametrize("file_path, min_hash_length", [
    (__file__, 32),  # Current file, typical hash length
    # Add more test files and expected hash lengths as needed
])
def test_verify_file_hash_valid(file_path, min_hash_length):
    result = verify_file_hash(file_path)
    assert isinstance(result, str), f"Expected string, got {type(result)}"
    assert len(result) >= min_hash_length, f"Hash length {len(result)} is less than {min_hash_length}"

def test_verify_file_hash_invalid():
    with pytest.raises(Exception):
        verify_file_hash("non_existent_file.txt")
