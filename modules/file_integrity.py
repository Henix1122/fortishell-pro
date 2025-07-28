import hashlib
import os

def get_supported_algorithms():
    """Return a list of supported hash algorithms."""
    return sorted(hashlib.algorithms_guaranteed)

def compute_file_hash(file_path, algo="sha256", chunk_size=8192):
    """
    Compute the hash of a file using the specified algorithm and chunk size.
    Returns the hex digest or raises an exception.
    """
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    try:
        hash_func = hashlib.new(algo)
    except ValueError:
        raise ValueError(f"Unsupported hash algorithm: {algo}")

    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(chunk_size), b""):
            hash_func.update(chunk)
    return hash_func.hexdigest()

def verify_file_hash(file_path, reference_hash, algo="sha256"):
    """
    Verify the file's hash against a reference hash.
    Returns True if matches, False otherwise.
    Raises exceptions for errors.
    """
    current_hash = compute_file_hash(file_path, algo)
    return current_hash == reference_hash

def check_integrity(file_path, reference_hash, algo="sha256"):
    """
    Check file integrity and return a detailed result dictionary.
    """
    result = {
        "File": os.path.basename(file_path),
        "Hash Algorithm": algo,
        "Current Hash": None,
        "Reference Hash": reference_hash,
        "Status": None,
        "Error": None
    }
    try:
        current_hash = compute_file_hash(file_path, algo)
        result["Current Hash"] = current_hash
        result["Status"] = "Match ✅" if current_hash == reference_hash else "Mismatch 🔥"
    except Exception as e:
        result["Error"] = str(e)
        result["Status"] = "Error ❌"
    return result

def print_integrity_report(report):
    """
    Pretty-print the integrity check report.
    """
    print(f"File: {report['File']}")
    print(f"Hash Algorithm: {report['Hash Algorithm']}")
    print(f"Current Hash: {report['Current Hash']}")
    print(f"Reference Hash: {report['Reference Hash']}")
    print(f"Status: {report['Status']}")
    if report.get("Error"):
        print(f"Error: {report['Error']}")

# Example usage:
# report = check_integrity("/path/to/file", "referencehash123", "sha256")
# print_integrity_report(report)
