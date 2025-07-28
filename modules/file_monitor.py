import hashlib
import os

def calculate_file_hash(file_path, hash_algo='sha256', chunk_size=4096):
    """
    Calculate the hash of a file using the specified algorithm.
    Supported algorithms: 'sha256', 'md5', 'sha1', etc.
    """
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    try:
        hasher = hashlib.new(hash_algo)
    except ValueError:
        raise ValueError(f"Unsupported hash algorithm: {hash_algo}")

    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(chunk_size), b''):
            hasher.update(chunk)
    return hasher.hexdigest()

def check_integrity(file_path, reference_hash, hash_algo='sha256'):
    """
    Check the integrity of a file by comparing its hash to a reference hash.
    Returns True if the file's hash matches the reference hash, False otherwise.
    """
    try:
        file_hash = calculate_file_hash(file_path, hash_algo)
        return file_hash == reference_hash
    except Exception as e:
        # Optionally log the error
        return False
