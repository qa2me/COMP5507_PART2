from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes

from signatures import hash_file, hash_message


# check a signature against a hash using the SENDER's public key.
# must use the same padding + hash algorithm that sign_file() used (PKCS1v15 + SHA256)
def verify_signature(file_hash, signature, public_key):
    try:
        public_key.verify(signature, file_hash, padding.PKCS1v15(), hashes.SHA256())
        return True
    except InvalidSignature:
        return False


# re-hash the file as it is NOW and check it against the signature.
# if even one byte of the file changed since signing, the hash changes and verification fails
def verify_file(file_path, signature, public_key):
    current_hash = hash_file(file_path).encode()
    return verify_signature(current_hash, signature, public_key)


# same idea for a typed message: hash it again and check it against the signature
def verify_message(message, signature, public_key):
    current_hash = hash_message(message).encode()
    return verify_signature(current_hash, signature, public_key)
