import hashlib


def calculate_sha256(file_path):
    """
    Calculate and return the SHA-256 hash of a file.
    """

    sha256_hash = hashlib.sha256()

    with open(file_path, "rb") as file:
        while chunk := file.read(4096):
            sha256_hash.update(chunk)

    return sha256_hash.hexdigest()
