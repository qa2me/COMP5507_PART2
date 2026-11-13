from key_generation import generate_keys
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
 
def encrypt_file(file_path,key):
    with open(file_path, 'rb') as file:
        plaintext = file.read()

    ciphertext = key.encrypt(plaintext,padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),algorithm=hashes.SHA256(),label=None))

    with open(file_path, 'wb') as file:
        file.write(ciphertext)

def decrypt_file(file_path, key):
    with open(file_path, 'rb') as file:
        ciphertext = file.read()

    plaintext = key.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    with open(file_path, 'wb') as file:
        file.write(plaintext)


if __name__ == "__main__":
    #create a pair of keys for alice and bob (generate_keys returns private first, then public)
    private_of_alice,public_of_alice = generate_keys()
    private_of_bob,public_of_bob = generate_keys()


    #usage of how to use when alice want to send to bob
    encrypt_file('qais.txt', public_of_bob)

    print("File After Encryption:")
    with open('qais.txt', 'rb') as file:
        content = file.read()
        print(content)
    decrypt_file('qais.txt', private_of_bob)

