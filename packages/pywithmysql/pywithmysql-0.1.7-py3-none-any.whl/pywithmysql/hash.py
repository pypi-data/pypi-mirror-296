import hashlib


def hash_passwd(password: str) -> str:
    """
    This function create SHA256 hash for password
    :param password: str -> password
    :return: str -> hash of password
    """
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

