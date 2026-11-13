import hashlib
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes

from key_generation import generate_keys

# getting the hash of the value of the given file
def hash_file(file_path):
    
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)

     
    return sha256_hash.hexdigest()


# encrypt the hash of the file with the key
def sign_file(file_hash, key):

    signature = key.sign(file_hash,padding.PKCS1v15(),hashes.SHA256())

    return signature

if __name__ == "__main__":
    prv,pub =generate_keys()
    # usage
    print("File Signature:", sign_file(hash_file('qais.txt').encode(), prv))


